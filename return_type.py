import sys
import numpy as np
import tensorflow as tf

from tensorflow import keras

def color(img_array):
    model = keras.models.load_model("./color_model.h5")
    predictions = model(img_array)
    # predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['black', 'blue', 'brown', 'green', 'grey', 'orange', 'pink', 'red', 'skyblue', 'violet', 'white', 'yellow']

    return(class_names[np.argmax(score)], np.argmax(score))

def category(img_array):
    model = keras.models.load_model("./category_model_mnist.h5")
    predictions = model(img_array)
    # predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['bottom', 'dress', 'outer', 'top']

    return (class_names[np.argmax(score)], np.argmax(score))

def length(img_array, type):
    if type == 'top':
        model = keras.models.load_model("./length_model_top.h5")
    if type == 'bottom':
        model = keras.models.load_model("./length_model_bottom.h5")
    if type == 'outer':
        model = keras.models.load_model("./length_model_outer.h5")
    if type == 'dress':
        model = keras.models.load_model("./length_model_dress.h5")
    predictions = model(img_array)
    # predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['long', 'middle', 'short']

    return (class_names[np.argmax(score)], np.argmax(score))

def fit(img_array, type):
    if type == 'top':
        model = keras.models.load_model("./fit_model_top.h5")
    if type == 'bottom':
        model = keras.models.load_model("./fit_model_bottom.h5")
    if type == 'outer':
        model = keras.models.load_model("./fit_model_outer.h5")
    if type == 'dress':
        model = keras.models.load_model("./fit_model_dress.h5")
    predictions = model(img_array)
    # predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['loose', 'normal', 'tight']

    return (class_names[np.argmax(score)], np.argmax(score))

def result(input):
    final = []
    img_height = 180
    img_width = 180

    test_path = input
    img = keras.preprocessing.image.load_img(test_path, target_size = (img_height, img_width))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    color_result, color_num = color(img_array)
    final.append(color_result)

    category_result, category_num = category(img_array)
    final.append(category_result)

    length_result, length_num = length(img_array, category_result)
    final.append(length_result)

    fit_result, fit_num = fit(img_array, category_result)
    final.append(fit_result)

    return final, color_num, category_num, length_num, fit_num #[color, category, length, fit]

def recommend(input):
    rec_arr = np.load("./rec_arr.npy")

    first = []
    second = []
    third = []
    x, color_num, category_num, length_num, fit_num = result(input)
    search = color_num * 36 + category_num * 9 + length_num * 3 + fit_num

    class_color = ['black', 'blue', 'brown', 'green', 'grey', 'orange', 'pink', 'red', 'skyblue', 'violet', 'white', 'yellow']
    class_category = ['bottom', 'dress', 'outer', 'top']
    class_length = ['long', 'middle', 'short']
    class_fit = ['loose', 'normal', 'tight']

    max = rec_arr[search].argmax()

    max_color =  max // 36
    first.append(class_color[max_color])

    if 0 <= max % 36 <= 8:
        max_category = 0
    elif 9 <= max % 36 <= 17:
        max_category = 1
    elif 18 <= max % 36 <= 26:
        max_category = 2
    else:
        max_category = 3
    first.append(class_category[max_category])

    if 0 <= max % 9 <= 2:
        max_length = 0
    elif 3 <= max % 9 <= 5:
        max_length = 1
    else:
        max_length = 2
    first.append(class_length[max_length])

    max_fit = max % 3
    first.append(class_fit[max_fit])

    for i in range(0, 432):
        for j in range(0, 432):
            if 36 * max_color <= j <= 36 * max_color + 35:
                rec_arr[i][j] = 0

    max = rec_arr[search].argmax()

    max_color = max // 36
    second.append(class_color[max_color])

    if 0 <= max % 36 <= 8:
        max_category = 0
    elif 9 <= max % 36 <= 17:
        max_category = 1
    elif 18 <= max % 36 <= 26:
        max_category = 2
    else:
        max_category = 3
    second.append(class_category[max_category])

    if 0 <= max % 9 <= 2:
        max_length = 0
    elif 3 <= max % 9 <= 5:
        max_length = 1
    else:
        max_length = 2
    second.append(class_length[max_length])

    max_fit = max % 3
    second.append(class_fit[max_fit])

    for i in range(0, 432):
        for j in range(0, 432):
            if 36 * max_color <= j <= 36 * max_color + 35:
                rec_arr[i][j] = 0

    max = rec_arr[search].argmax()

    max_color = max // 36
    third.append(class_color[max_color])

    if 0 <= max % 36 <= 8:
        max_category = 0
    elif 9 <= max % 36 <= 17:
        max_category = 1
    elif 18 <= max % 36 <= 26:
        max_category = 2
    else:
        max_category = 3
    third.append(class_category[max_category])

    if 0 <= max % 9 <= 2:
        max_length = 0
    elif 3 <= max % 9 <= 5:
        max_length = 1
    else:
        max_length = 2
    third.append(class_length[max_length])

    max_fit = max % 3
    third.append(class_fit[max_fit])

    return first, second, third