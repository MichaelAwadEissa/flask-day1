from flask import Flask, abort, url_for, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# start sql
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# (id, name, description , image)
class Blogs(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(250))

    def __str__(self):
        return f"{self.name}"

    @property
    def image_url(self):
        return url_for("static", filename=f"assets/images/blogs/{self.image}")

    @property
    def delete_url(self):
        return url_for("blogs.delete", blog=self.id)

    # @property
    # def show_url(self):
    #     return url_for("blogs.show", blog=self.id)


@app.route("/", endpoint="blogs.list")
def blogs_list():
    blogs = Blogs.query.all()
    return render_template("blogs/list.html", blogs=blogs)


@app.route("/blogs/create", endpoint="blogs.create", methods=["GET", "POST"])
def blogs_create():
    print(request.method, request.form)
    if request.method == "POST":
        blog = Blogs(
            name=request.form["name"],
            description=request.form["description"],
            image=request.form["image"],
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("blogs.list"))

    return render_template("blogs/create.html")


with app.app_context():
    db.create_all()


@app.route("/blogs/<int:blog>/update", endpoint="blogs.update", methods=["GET", "POST"])
def blogs_update(blog):
    blog = db.get_or_404(Blogs, blog)
    if request.method == "POST":
        # print("requested blog----------->\n", request.form)
        # print("-==->", request.POST["name"])
        # print("-==->", request.form["name"])
        blogobj = blog
        blogobj.name = request.form["name"]
        blogobj.description = request.form["description"]
        blogobj.image = request.form["image"]
        db.session.add(blogobj)
        db.session.commit()
        return redirect(url_for("blogs.list"))

    return render_template("blogs/update.html", blog=blog)


@app.route("/blogs/<int:blog>", endpoint="blogs.show")
def blogs_list(blog):
    blog = db.get_or_404(Blogs, blog)
    return render_template("blogs/show.html", blog=blog)


@app.route("/blogs/<int:blog>/delete", endpoint="blogs.delete")
def blogs_delete(blog):
    blog = db.get_or_404(Blogs, blog)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("blogs.list"))


@app.errorhandler(404)
def error_not_found(error):
    return render_template("errors/404.html")


# start server
if __name__ == "__main__":
    app.run(debug=True)
