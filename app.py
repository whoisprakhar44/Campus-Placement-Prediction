from flask import Flask, request, render_template
import pickle

pickle_in = open('campusplace_lr.pkl', 'rb')
lr = pickle.load(pickle_in)
pickle_in.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getting():

    if request.method == 'POST':

        my_dict = request.form
        gender = int(my_dict['gender'])
        spec = int(my_dict['spec'])
        tech = int(my_dict['tech'])
        work = int(my_dict['work'])
        ssc = float(my_dict['ssc'])
        hsc = float(my_dict['hsc'])
        dsc = float(my_dict['dsc'])
        mba = float(my_dict['mba'])

        features = [[gender, spec, tech, work, ssc, hsc, dsc, mba]]

        pred = lr.predict(features)

        pred_prob = lr.predict_proba(features)

        if pred[0]==1:
            prob = pred_prob[0][1]
        else:
            prob = pred_prob[0][0]

        print(pred, prob*100)

        place_dict = {1: "You'll be PLACED", 0: "Won't be Placed"}
        pred_class = place_dict[pred[0]]

        if pred[0] == 1:
            return render_template('show.html',pred_class=pred_class, pred_prob = round(prob*100, 2), placed=True)

        else:
            return render_template('show.html', pred_class=pred_class, pred_prob = round(prob*100, 2))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)