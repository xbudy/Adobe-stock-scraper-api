from fastapi import FastAPI
import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi.responses import FileResponse
from config import get_data
app = FastAPI()


@app.get("/get")
async def main(key:str):
    data=get_data(key)
    with open('ex.csv','w') as f:
      f.write(data)
    response=FileResponse('ex.csv',media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)
