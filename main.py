import uvicorn

from fastapi import FastAPI
from infrastructure.kafka.consumer import start_kafka_consumer, kafka_stop_consume
from presentation.api.routes import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await start_kafka_consumer()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_stop_consume()


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5050)