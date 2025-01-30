from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import Flask, request, jsonify, render_template, redirect, url_for
from bson import ObjectId  # ObjectId'yi import et

app = Flask(__name__)

# Azure Cosmos DB MongoDB URI
MONGO_URI = "your database URI"
try:
    client = MongoClient(MONGO_URI)
    db = client.bookstore
    collection = db.books
    print("MongoDB'ye başarıyla bağlanıldı!")
except ConnectionFailure as e:
    print(f"Bağlantı hatası: {e}")


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        data = request.form
        try:

            book_data = {
                "title": data['title'],
                "author": data['author'],
                "price": data['price'],
                "isbn": data['isbn']
            }
            result = collection.insert_one(book_data)
            return redirect(url_for('hello_world'))  # Redirect to home page after successful insert
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    return render_template('create.html')


@app.route('/read/<document_id>', methods=['GET'])
def read(document_id):
    try:
        # document_id'yi ObjectId'ye dönüştür
        document = collection.find_one({"_id": ObjectId(document_id)})
        if document:
            return render_template('read.html', document=document)
        return jsonify({"message": "Document not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/update/<document_id>', methods=['GET', 'POST'])
def update(document_id):
    if request.method == 'GET':
        document = collection.find_one({"_id": ObjectId(document_id)})
        if document:
            return render_template('update.html', document=document)
        return jsonify({"message": "Document not found"}), 404
    elif request.method == 'POST':
        data = request.form.to_dict()  # Form verisini dictionary formatında al

        # Mevcut belgeyi almak
        current_document = collection.find_one({"_id": ObjectId(document_id)})
        if not current_document:
            return jsonify({"message": "Document not found"}), 404

        # Değişiklik olup olmadığını kontrol et
        changes_made = False
        for key, value in data.items():
            if current_document.get(key) != value:
                changes_made = True
                break  # İlk değişikliği bulduğumuzda döngüden çıkıyoruz

        # Eğer değişiklik yapılmadıysa
        if not changes_made:
            return jsonify({"message": "No changes made"}), 400  # Ya da uygun bir mesaj

        # Güncelleme işlemi
        result = collection.update_one({"_id": ObjectId(document_id)}, {"$set": data})
        if result.modified_count > 0:
            return redirect(url_for('read', document_id=document_id))
        else:
            return jsonify({"message": "No changes made or document not found"}), 404


@app.route('/delete/<document_id>', methods=['GET', 'POST'])
def delete(document_id):
    if request.method == 'GET':
        return render_template('delete.html', document_id=document_id)
    elif request.method == 'POST':
        try:
            result = collection.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count > 0:
                return redirect(url_for('hello_world'))  # Redirect to the home page after deletion
            return jsonify({"message": "Document not found"}), 404
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/books', methods=['GET'])
def books():
    try:
        books_list = collection.find()  # Veritabanındaki tüm kitapları çekiyoruz
        books_list = list(books_list)  # Cursor'ı listeye çeviriyoruz

        # Debug amacıyla kitapları yazdırıyoruz.
        print("Books List:", books_list)

        return render_template('books.html', books=books_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
