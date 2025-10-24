rom fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import io

app = FastAPI(title="Excel Reviews Analyzer API", version="1.0")

@app.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"
    ]:
        raise HTTPException(status_code=400, detail="Пожалуйста, загрузите файл Excel (.xls или .xlsx).")

    try:
        excel_bytes = await file.read()
        df = pd.read_excel(io.BytesIO(excel_bytes), engine="openpyxl")
        reviews_count = df.shape[0]

        review_column = None
        for col in df.columns:
            if "review" in col.lower():
                review_column = col
                break

        avg_length = df[review_column].astype(str).str.len().mean() if review_column else "Колонка с отзывами не найдена"

        return {
            "Количество отзывов": reviews_count,
            "Средняя длина отзыва": avg_length
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")
