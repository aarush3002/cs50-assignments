import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}
    
    linked_pages = corpus[page]
    
    for x in corpus.keys():
        if x in linked_pages:
            result[x] = damping_factor * float(1/len(linked_pages))
        else:
            result[x] = 0.00
    
    damp = (1 - damping_factor)/len(corpus)
    
    for key in result:
        result[key] += damp
    
    return result
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    pages = list(corpus.keys())
    for key in pages:
        result[key] = 0
    curr_samp = random.choice(pages)
    result[curr_samp] += 1
    for x in range(n - 1):
        trans = transition_model(corpus, curr_samp, damping_factor)
        curr_samp = random.choices(
            population = list(trans.keys()),
            weights = list(trans.values()),
            k = 1
        )
        curr_samp = curr_samp[0]
        result[curr_samp] += 1
    
    for key in result:
        result[key] = float(result[key] / n)

    return result
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    for pg in corpus.keys():
        result[pg] = float(1/len(corpus.keys()))

    flag = False
    while not flag:
        to_result = {}

        flag = True
        for i in result.keys():
            temp = result[i]
            to_result[i] = float((1-damping_factor)/len(corpus.keys()))
            for page, links in corpus.items():
                if i in links:
                    to_result[i] += float(damping_factor*result[page]/len(links))
            if abs(temp - to_result[i]) > 0.001:
                flag = False
        for i in result.keys():
            result[i] = to_result[i]

    return result
    #raise NotImplementedError


if __name__ == "__main__":
    main()
