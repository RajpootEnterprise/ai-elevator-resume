from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

skills_db = [
    "python",
    "react",
    "javascript",
    "html",
    "css",
    "node",
    "docker",
    "sql"
]


def analyze_resume(text):

    detected = []

    for skill in skills_db:

        if skill in text.lower():
            detected.append(skill)

    missing = list(set(skills_db) - set(detected))

    score = int((len(detected) / len(skills_db)) * 100)

    return {
        "score": score,
        "skills_detected": detected,
        "missing_skills": missing
    }


@app.get("/")
def home():
    return {"message": "Vidyamantra AI Backend Running"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    content = await file.read()

    text = content.decode(errors="ignore")

    result = analyze_resume(text)

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
