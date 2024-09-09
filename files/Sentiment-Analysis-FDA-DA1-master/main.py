# Run "pip install -r requirement.txt" and install all the required packages

from flask import Flask, render_template, request
import services
import os
import matplotlib.pyplot as plt

STATIC_FOLDER = 'templates/assets'
app = Flask(__name__, static_folder=STATIC_FOLDER)

@app.route('/')
def hello_world():
   return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
   link = request.form['link']
   comments = int(request.form['comments'])
   result = services.main(link, comments)

   # print(result)

   pList = result['positive']
   nList = result['negative']
   neList = result['neutral']
   total = len(pList) + len(nList) + len(neList)
   pListPercent = round(len(pList)/total*100, 2)
   nListPercent = round(len(nList)/total*100, 2)
   neListPercent = round(len(neList)/total*100, 2)
   title = result['title']
   thumbnail = result['thumbnail']

   # fig = Figure()
   # ax = fig.subplots()
   # ax.plot([1, 2])
   # buf = BytesIO()
   # fig.savefig(buf, format="png")

   categories = [f'Positive ({len(pList)})', f'Negative ({len(nList)})', f'Neutral ({len(neList)})']
   values = [pListPercent, nListPercent, neListPercent]
   plt.pie(values, labels=categories, autopct='%1.1f%%')
   os.remove('templates/assets/sentiment.png')
   plt.savefig('templates/assets/sentiment.png')
   plt.close()
   
   return render_template('result.html', title=title, thumbnail=thumbnail, img_url='/assets/sentiment.png')
   # return result
   
if __name__ == '__main__':
   app.run(debug=True)