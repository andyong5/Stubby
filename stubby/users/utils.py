from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.file_name)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, '/static/profile_pic', picture_fn)
    output_size(125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
