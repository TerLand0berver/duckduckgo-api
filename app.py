from itertools import islice
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

def extract_search_params(request):
    if request.method == 'POST':
        keywords = request.form['q']
        max_results = int(request.form.get('max_results', 10))
    else:
        keywords = request.args.get('q', '')  # 提供默认值以避免 None
        max_results = int(request.args.get('max_results', 10))
    return keywords, max_results

@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        keywords, max_results = extract_search_params(request)
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(keywords, safesearch='Off', timelimit='y', backend="lite")
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@app.route('/searchAnswers', methods=['GET', 'POST'])
def search_answers():
    try:
        keywords, max_results = extract_search_params(request)
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.answers(keywords)
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@app.route('/searchImages', methods=['GET', 'POST'])
def search_images():
    try:
        keywords, max_results = extract_search_params(request)
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.images(keywords, safesearch='Off', timelimit=None)
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@app.route('/searchVideos', methods=['GET', 'POST'])
def search_videos():
    try:
        keywords, max_results = extract_search_params(request)
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.videos(keywords, safesearch='Off', timelimit=None, resolution="high")
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
