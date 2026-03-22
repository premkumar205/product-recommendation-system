import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_excel(r"C:\Users\yadav\OneDrive\Documents\abc\backend\product_dataset_1500_rows.xlsx")

# Clean data
df.fillna('', inplace=True)

# Convert to string
cols = ['Product_Name', 'Category', 'Brand', 'Description']
for col in cols:
    df[col] = df[col].astype(str)

# Remove duplicates (IMPORTANT)
df = df.drop_duplicates(subset=['Product_Name', 'Brand'])

# Create combined text (IMPROVED)
df['combined_text'] = (
    df['Product_Name'] + " " +
    df['Category'] * 2 + " " +
    df['Brand'] * 2 + " " +
    df['Description']
)

# TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_text'])

# Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_products(product_id, top_n=6):
    try:
        idx = df[df['Product_ID'] == product_id].index[0]

        scores = list(enumerate(cosine_sim[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Remove same product
        scores = scores[1:]

        # Get top N
        product_indices = [i[0] for i in scores[:top_n]]

        return df.iloc[product_indices][[
            'Product_ID',
            'Product_Name',
            'Category',
            'Brand',
            'Price',
            'Rating',
            'Image_URL'
        ]].to_dict(orient='records')

    except:
        return []