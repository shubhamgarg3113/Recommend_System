# Movie Recommendation System

This project is a **content-based movie recommendation system** built using Python, Pandas, and Scikit-learn. It processes movie data from the TMDB 5000 dataset to recommend similar movies based on various features such as genres, cast, crew, keywords, and movie overviews.

## 📁 Dataset Used

The system uses two CSV files:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

Both datasets are loaded from Google Drive within the notebook.

## 🛠 Features Extracted

The following features are extracted and combined into a single `tags` field:

* Genres
* Keywords
* Cast (Top 3 actors)
* Crew (Director only)
* Overview (Plot summary)

## ⚙️ Processing Steps

1. **Data Cleaning**: Removed null values and duplicates.
2. **Feature Engineering**: Parsed JSON-like strings into Python lists using `ast.literal_eval()`.
3. **Text Preprocessing**:

   * Concatenated all selected features into a single string (`tags`)
   * Applied stemming using `PorterStemmer`
   * Converted all text to lowercase
4. **Vectorization**: Used `CountVectorizer` with max 5000 features and English stop words removal.
5. **Similarity Calculation**: Used cosine similarity to compute pairwise similarities between movies.

## 🎯 Functionality

A function `recommend(movie)` is defined, which returns a list of the top 5 most similar movies based on content similarity.

## 📦 Libraries Used

* `pandas`
* `numpy`
* `ast`
* `nltk`
* `sklearn`
* `google.colab` (for mounting Google Drive)

## 🚀 How to Run

1. Upload the dataset files to your Google Drive.
2. Run the notebook in Google Colab.
3. Ensure NLTK stopwords and PorterStemmer are available (they are preloaded in Colab).
4. Call the `recommend('Movie Title')` function with a valid movie title from the dataset.

## 📌 Example Usage

```python
recommend("Avatar")
```

## 🔍 Future Improvements

* Add support for collaborative filtering or hybrid methods.
* Deploy using a web framework like Flask or Streamlit.
* Use TF-IDF or advanced embeddings like BERT for better semantic understanding.
