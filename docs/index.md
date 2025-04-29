# Using fastapi-sio

This doc page provides a short guide to the fastapi-sio library. It includes instructions for integrating fastapi-sio with FastAPI, details on using emitters for Socket.IO channels, and guidance on generating and using AsyncAPI documentation. Use this page as the main entry point for understanding and utilizing the features of fastapi-sio in your projects.

## Using with FastAPI

To get started, install the library and set up your FastAPI app as usual. Then, create a `FastAPISIO` instance and mount it to your FastAPI application.

**Example:**

```python
fastapi = FastAPI()
sio = FastAPISIO(app=fastapi)

# Mount the ASGI app
app = sio.asgi_app

@fastapi.get("/")
async def example_fastapi_route():
    return {"message": "Welcome to the FastAPI-SIO example!"}
```

Run the ASGI app provided by FastAPISIO.asgi_app. Socket.io traffic will be handled by _socketio_, while the rest by _FastAPI_.

---

## Using Emitters

Emitters allow you to send data to clients on specific Socket.IO channels, with full type safety and schema validation.

**How to use:**

1. **Define a Pydantic model** for the data you want to emit.
2. **Create an emitter** using `sio.create_emitter("event_name", model=YourModel)`.
3. **Emit data** by calling `await emitter.emit(payload)` inside your handler.

**Example:**

```python
class Notification(BaseModel):
    message: str

notifier = sio.create_emitter("notify", model=Notification)

@sio.on("ping")
async def handle_ping(sid, data):
    await notifier.emit(Notification(message="pong!"))
```

- The emitted data will be validated and serialized according to your Pydantic model.

---

## AsyncAPI Documentation

`fastapi-sio` automatically generates an [AsyncAPI](https://www.asyncapi.com/) specification for your Socket.IO events and data models.

### How to access the documentation

- By default, the AsyncAPI spec is available at:  
  `GET /sio/docs/asyncapi.json`

### How to use the documentation

1. **Start your FastAPI app.**
2. **Open the `/sio/docs/asyncapi.json` endpoint** in your browser or with a tool like `curl`.
3. **Copy the JSON output.**
4. **Paste it into the [AsyncAPI Studio](https://studio.asyncapi.com/)** online to view and interact with your API documentation.

> [!NOTE]  
> Currently, `fastapi-sio` does not self-host the AsyncAPI Studio UI. You must manually copy the JSON and use the AsyncAPI online tools.
