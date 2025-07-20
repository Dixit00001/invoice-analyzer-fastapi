from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Read PDF using pdfplumber
    contents = await file.read()

    sum_total = 0
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and row[0] == "Doodad":
                        try:
                            sum_total += int(row[-1])  # Last column is 'Total'
                        except ValueError:
                            pass  # Skip headers or malformed rows

    return JSONResponse(content={"sum": sum_total})
