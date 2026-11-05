# Project Notes

## How `navigator.geolocation` works and helps this app

`navigator` is a browser-provided object for browser features. Its `geolocation`
property exposes the Geolocation API when the browser supports it. The API can
ask the user for permission to access the device's location and, if permission is
granted, provide coordinates. Geolocation generally requires a secure context
(HTTPS; `localhost` is also treated as secure by browsers).

In [`templates/chat.html`](./templates/chat.html), the page checks whether
`navigator.geolocation` exists, then calls
`navigator.geolocation.getCurrentPosition(...)` once when the page loads. This
call is asynchronous: the browser invokes the success callback later, after it
gets a position. The callback copies `position.coords.latitude` and
`position.coords.longitude` into hidden form inputs. Those values are submitted
with the chat message; they are not sent to the server by the geolocation call
itself.

The flow through this codebase is:

1. The browser obtains coordinates, with the user's permission.
2. The chat form posts the hidden `latitude` and `longitude` fields to `/send`.
3. [`web_app.py`](./web_app.py) reads those fields and saves them in the Flask
   session as `user_session`.
4. The `get_location` tool in [`tools/tools_live.py`](./tools/tools_live.py)
   reads those coordinates and reverse-geocodes them with OpenStreetMap
   Nominatim to derive a city and country. The weather agent can use that
   location when a weather question does not name a city.

For example, the essential browser-side operation is:

```javascript
navigator.geolocation.getCurrentPosition(function (position) {
    const { latitude, longitude } = position.coords;
    document.getElementById('latitude').value = latitude;
    document.getElementById('longitude').value = longitude;
});
```

### Practical considerations

- The user can deny permission, the browser may not support geolocation, or the
  location request may fail. The current page does not provide an error callback
  or a user-facing error message.
- Since the result arrives asynchronously, a user who submits the form before
  the callback runs may send empty coordinates. The current handler only
  replaces the saved session location when both submitted values are present.
- Coordinates are sensitive location data. Request them only when needed,
  explain their use, and avoid retaining or sharing them beyond the app's
  requirements.

## How Jinja2 templates work and how this app uses them

The template engine used by Flask is **Jinja2** (not “Ginger 2”). A Jinja
template is mostly ordinary HTML with special tags that let the server insert
data and conditionally generate parts of the page before sending the finished
HTML to the browser.

The main Jinja syntax used here is:

- `{{ expression }}` evaluates an expression and inserts its value into the
  rendered HTML.
- `{% ... %}` runs template logic, such as an `if` statement or a loop. These
  tags control rendering and do not themselves appear in the output.
- `{# ... #}` marks a Jinja comment, which is omitted from the rendered output.

In [`web_app.py`](./web_app.py), the `/` route calls
`render_template('chat.html', messages=...)`. Flask finds `chat.html` in the
`templates` directory and makes the `messages` value available to that
template. On a new session it is an empty list; after chat submissions it
contains message dictionaries with a `type` and `content`.

In [`templates/chat.html`](./templates/chat.html), the template checks whether
`messages` contains anything. If it does, it loops over the messages and uses
the `type` to choose the appropriate CSS class. If the list is empty, the
template renders the “Ask me about the weather!” prompt instead.

For example, this simplified version illustrates the same pattern:

```jinja
{% if messages %}
    {% for msg in messages %}
        <div class="message {{ 'user' if msg.type == 'human' else 'agent' }}">
            {{ msg.content }}
        </div>
    {% endfor %}
{% else %}
    <p>Ask me about the weather!</p>
{% endif %}
```

In the actual page, separate `if`/`elif` branches render `human` and `ai`
messages as `message user` and `message agent` elements, respectively. Their
CSS rules style those messages differently. Jinja's autoescaping is enabled by
default for HTML templates, so values such as `msg.content` are escaped when
inserted into HTML; they are displayed as text instead of being interpreted as
HTML markup.

## What `@contextmanager` does and how `create_agent_instance` works

A context manager sets up a resource, makes it available for a limited period,
and then cleans it up. The familiar `with` statement uses this lifecycle:

```python
with open("notes.txt") as file:
    text = file.read()
# The file is closed automatically here.
```

`@contextmanager` from Python's `contextlib` lets a generator function provide
the same setup/use/cleanup pattern without defining a class. Code before the
function's `yield` is setup; the yielded value is assigned to the name after
`as`; when the `with` block exits, execution resumes after `yield` so cleanup
can run. If the block raises an exception, the context manager is also exited,
allowing its resource cleanup to run.

In [`utils/agent_utils.py`](./utils/agent_utils.py),
`create_agent_instance` uses this pattern to tie the lifetime of an agent to
the SQLite checkpointer it needs:

1. `SqliteSaver.from_conn_string(checkpoint_path)` opens/creates the SQLite
   checkpointer resource (by default, `sqlite/checkpoints.db`).
2. `create_agent(...)` builds an agent configured with the model from
   `create_llm()`, the weather and location tools, the system prompt, and that
   checkpointer.
3. `yield` hands the configured agent to the caller while keeping the
   checkpointer's `with` block open. The checkpointer can therefore persist
   conversation state while the agent is being used.
4. When the outer context manager is exited, the SQLite checkpointer's own
   context manager closes its resource.

The `@contextmanager` wrapper means callers use it as a context manager rather
than treating it as a function that directly returns an agent:

```python
with create_agent_instance() as agent:
    result = invoke_agent(agent, "What's the weather in Paris?", "thread-123")
```

The current module creates a long-lived instance at import time:

```python
agent_context = create_agent_instance()
agent = agent_context.__enter__()
```

[`weather_app.py`](./weather_app.py) imports this global `agent` and passes it
to `invoke_agent` for each `/send` request. `invoke_agent` packages the user's
text as a user message and calls `agent.invoke`. It also passes the session's
`thread_id` as configurable metadata. The checkpointer uses that ID to keep
separate conversation state for separate Flask sessions while allowing each
session's conversation to continue across requests.

Calling `__enter__()` manually starts the managed lifetime, but this module
does not call `agent_context.__exit__()`. As a result, the checkpointer is
left open for the life of the application process; the `with` block inside
`create_agent_instance` only finishes once that context manager is exited. If
the application later needs controlled shutdown or short-lived agents, pair
entry and exit explicitly (or use a `with create_agent_instance()` block around
the agent's complete period of use).
