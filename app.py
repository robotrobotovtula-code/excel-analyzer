from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import io

app = FastAPI(title="Модуль анализа отзывов мебельного магазина")

@app.post("/analyze")
async def analyze_reviews(file: UploadFile = File(...)):
    # Проверка типа файла
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
        "application/vnd.ms-excel"  # .xls
    ]:
        raise HTTPException(status_code=400, detail="Пожалуйста, загрузите файл Excel (.xlsx или .xls)")

    try:
        # Читаем байты файла
        excel_bytes = await file.read()

        # Загружаем в pandas DataFrame
        df = pd.read_excel(io.BytesIO(excel_bytes), engine="openpyxl")
        
        # Анализ: считаем количество отзывов
        reviews_count = df.shape[0]
        
        # Ищем колонку с отзывами
        review_column = None
        for col in df.columns:
            if "отзыв" in col.lower() or "review" in col.lower():
                review_column = col
                break
        
        # Вычисляем среднюю длину текста отзывов
        if review_column:
            avg_length = df[review_column].astype(str).str.len().mean()
        else:
            avg_length = "Колонка с отзывами не найдена"

        return {
            "Общее количество отзывов": reviews_count,
            "Средняя длина отзыва": avg_length
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")
