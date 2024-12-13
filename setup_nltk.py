import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 必要なすべてのNLTKリソースをダウンロード
resources = [
    'punkt',
    'punkt_tab',
    'averaged_perceptron_tagger',
    'maxent_ne_chunker',
    'words',
    'stopwords'
]

for resource in resources:
    try:
        nltk.download(resource)
        print(f"Successfully downloaded {resource}")
    except Exception as e:
        print(f"Error downloading {resource}: {e}")

# ダウンロードしたデータの場所を確認
import os
nltk_data_path = nltk.data.path
print("\nNLTK Data Paths:")
for path in nltk_data_path:
    print(f"- {path}")