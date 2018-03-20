from clarifai.rest import ClarifaiApp


def get_keywords_from_image(url_of_image):

    app = ClarifaiApp(api_key='c454678d5220482da00c78696f1d92ca')
    app.models.search(model_name='general-v1.3', model_type='concept')

    model = app.models.get('My model')

    response = model.predict_by_url(url=url_of_image)
    return response

