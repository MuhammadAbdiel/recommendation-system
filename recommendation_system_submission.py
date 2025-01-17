# -*- coding: utf-8 -*-
"""Recommendation_System_Submission.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dlU4xJIg8VjTr2mOcAP-foFLW5n5d6UM

# **Muhammad Abdiel Firjatullah**

# **Recommendation System - Rekomendasi Judul Film Berdasarkan Genre**

# **Deskripsi Proyek**

Pada proyek kali ini sebuah perusahaan yang bergerak di industri perfilman ingin meningkatkan traffic platform film streaming mereka, oleh karena itu perusahaan akan mencoba menerapkan pendekatan Machine Learning untuk merekomendasi film-film yang mereka sediakan berdasarkan genre filmnya.

# **1. Import Library yang Dibutuhkan**

## Install Public  API Kaggle
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install -q kaggle

"""## Install library untuk proses data loading dan visualisasi data"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""# **2. Data Understanding**

Data Understanding merupakan proses memahami informasi dalam data dan menentukan kualitas dari data tersebut.

## **2.1 Data Loading**

Data Loading merupakan tahap untuk memuat dataset yang akan digunakan agar dataset lebih mudah dipahami.             


*Dataset yang digunakan pada proyek ini:*  
https://www.kaggle.com/datasets/gargmanas/movierecommenderdataset
"""

# Membuat direktori baru bernama kaggle
!rm -rf ~/.kaggle && mkdir ~/.kaggle/

# Menyalin berkas kaggle.json pada direktori aktif saat ini ke direktori kaggle
!mv kaggle.json ~/.kaggle/kaggle.json

# Mengubah permission berkas
!chmod 600 ~/.kaggle/kaggle.json

# Download dataset
!kaggle datasets download -d gargmanas/movierecommenderdataset

# Ekstrak berkas zip
!unzip /content/movierecommenderdataset.zip

"""## Melihat isi dataset movies.csv"""

movies = pd.read_csv('/content/movies.csv')
values = ['Comedy','Action','Adventure','Documentary','Horror','Crime','Drama','Romance','Thriller','Mystery', 'Animation', 'Fantasy']
movies = movies[movies.genres.isin(values) == True]

movies

"""## Melihat isi dataset ratings.csv"""

rating = pd.read_csv('/content/ratings.csv')
rating

"""### **2.2 Exploratory Data Analysis (EDA)**

Exploratory data analysis merupakan proses investigasi awal pada data untuk menganalisis karakteristik, menemukan pola, anomali, dan memeriksa asumsi pada data

#### **2.2.1 EDA - Deskripsi Variabel**

## Melihat informasi pada dataset movies
"""

movies.info()

"""## Melihat informasi pada dataset ratings"""

rating.info()

"""#### **2.2.2 EDA - Univariate Analysis**

##### **- Movies**
"""

# Melihat jumlah film dan jumlah genre yang ada beserta nama genrenya
print('Jumlah Film: ', len(movies.movieId.unique()))
print('Jumlah genre: ', len(movies.genres.unique()))
print('Genre: ', movies.genres.unique())

"""## Visualisasi fitur 'genres' untuk melihat pembagian isi datasetnya"""

categorical_features = ['genres']
feature = categorical_features[0]
count = movies[feature].value_counts()
percent = 100*movies[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah film':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature)

"""##### **- Rating**"""

# Melihat jumlah userID dan jumlah data rating
print('Jumlah userID: ', len(rating.userId.unique()))
print('Jumlah data rating: ', len(rating))

"""## Visualisasi fitur numerik yang ada di dataset rating"""

rating.hist(bins=50, figsize=(20,15))
plt.show()

"""## **3. Data Preparation**

Data Preparation merupakan tahap untuk mempersiapkan data sebelum masuk ke tahap pembuatan model Machine Learning.

### **3.1 Menggabungkan Dataset dan Menangani Missing Value**
"""

# Menggabungkan dataset movies dan rating
all_movies = pd.merge(movies, rating, on='movieId', how='left')
all_movies

"""## Melihat data yang kosong"""

all_movies.isnull().sum()

"""## Membuang data yang kosong"""

all_movies_clean = all_movies.dropna()
all_movies_clean

"""## Menampilkan data dan mengurutkannya berdasarkan movieId"""

fix_movies = all_movies_clean.sort_values('movieId', ascending=True)
fix_movies

"""## Melihat berapa jumlah film dalam fix_movies"""

len(fix_movies.movieId.unique())

"""## Melihat genre movie setelah data dirapihkan"""

print('Genre: ', fix_movies.genres.unique())

"""### **3.2 Menghapus Data Duplikat**"""

# Menghapus data duplikat pada variabel preparation
preparation = fix_movies.drop_duplicates('movieId')
preparation

"""### **3.3 Mengonversi Data Series Menjadi Bentuk List**"""

# Mengonversi data series ‘movieId’ menjadi bentuk list
movie_id = preparation['movieId'].tolist()

# Mengonversi data series ‘title’ menjadi bentuk list
movie_title = preparation['title'].tolist()

# Mengonversi data series ‘genres’ menjadi bentuk list
movie_genre = preparation['genres'].tolist()

print(len(movie_id))
print(len(movie_title))
print(len(movie_genre))

"""## Membuat dictionary data"""

movie_new = pd.DataFrame({
    'id': movie_id,
    'movie_title': movie_title,
    'genre': movie_genre
})
movie_new

"""## Melihat 5 sampel movie"""

data = movie_new
data.sample(5)

"""## **4. Model Development - Content Based Filtering**

Ide dari sistem rekomendasi berbasis konten (content-based filtering) adalah merekomendasikan item yang mirip dengan item yang disukai pengguna di masa lalu.

### **4.1 TF-IDF Vectorizer**
"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data genre
tf.fit(data['genre'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

"""## Melakukan fit lalu ditransformasikan ke bentuk matrix dan Melihat ukuran matrix TF-IDF"""

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(data['genre'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

"""## Mengubah vektor TF-IDF dalam bentuk matriks dengan fungsi todense()"""

tfidf_matrix.todense()

"""## Membuat dataframe untuk melihat TF-IDF matrix"""

# Kolom diisi dengan genre
# Baris diisi dengan movie title

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names_out(),
    index=data.movie_title
).sample(12, axis=1).sample(10, axis=0)

"""### **4.2 Cosine Similarity**

## Menghitung cosine similarity pada matrix TF-IDF
"""

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

"""## Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa movie title"""

cosine_sim_df = pd.DataFrame(cosine_sim, index=data['movie_title'], columns=data['movie_title'])
print('Shape:', cosine_sim_df.shape)

"""## Melihat similarity matrix pada setiap movie title"""

cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""### **4.3 Membuat Fungsi movie_recommendation()**"""

def movie_recommendations(movie_title, similarity_data=cosine_sim_df, items=data[['movie_title', 'genre']], k=10):
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,movie_title].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Membuang movie_title agar nama film yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(movie_title, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

"""### **4.4. Result**

## Melihat genre film yang akan diuji
"""

movie_title = 'Piper (2016)'
data[data.movie_title.eq(movie_title)]

"""## Menampilkan hasil rekomendasi judul film berdasarkan genre"""

movie_title = 'Piper (2016)'
movie_recommendations = movie_recommendations(movie_title)
movie_recommendations

"""## **5. Evaluation**

Metrik yang cocok dipakai untuk kasus content based filtering adalah ***Precision***, yang dapat dirumuskan sebagai berikut:

![img](https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/academy/dos:819311f78d87da1e0fd8660171fa58e620211012160253.png)

Berdasarkan hasil di atas dapat disimpulkan bahwa dari 10 judul film yang direkomendasikan, ada 10 item yang relevan, oleh karena itu ***Precision*** dari model tersebut adalah 10/10 atau 100%
"""