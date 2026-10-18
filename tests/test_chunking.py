from ResearchSummarizer.pipeline import prediction_pipeline as pp
from ResearchSummarizer.pipeline.prediction_pipeline import PredictionPipeline


class WordTokenizer:
    """Stub tokenizer: one token per whitespace-separated word."""

    def __init__(self):
        self.vocab: dict[str, int] = {}
        self.inverse: dict[int, str] = {}

    def __call__(self, text, add_special_tokens=False):
        ids = []
        for word in text.split():
            if word not in self.vocab:
                self.vocab[word] = len(self.vocab)
                self.inverse[self.vocab[word]] = word
            ids.append(self.vocab[word])
        return {"input_ids": ids}

    def decode(self, ids, skip_special_tokens=True):
        return " ".join(self.inverse[i] for i in ids)


def make_pipeline(max_tokens=10, overlap=3, monkeypatch=None):
    pipe = PredictionPipeline.__new__(PredictionPipeline)  # skip model loading
    pipe.tokenizer = WordTokenizer()
    pipe.max_input_tokens = max_tokens
    monkeypatch.setattr(pp, "CHUNK_OVERLAP_TOKENS", overlap)
    return pipe


def words(n):
    return " ".join(f"w{i}" for i in range(n))


def test_chunks_cover_all_tokens_with_overlap(monkeypatch):
    pipe = make_pipeline(max_tokens=10, overlap=3, monkeypatch=monkeypatch)
    chunks = pipe._chunk_text(words(25))

    assert all(len(c.split()) <= 10 for c in chunks)
    assert chunks[0].split()[-3:] == chunks[1].split()[:3]  # windows overlap
    covered = {w for c in chunks for w in c.split()}
    assert covered == set(words(25).split())
    assert chunks[-1].split()[-1] == "w24"


def test_short_text_is_a_single_chunk(monkeypatch):
    pipe = make_pipeline(max_tokens=10, overlap=3, monkeypatch=monkeypatch)
    assert pipe._chunk_text(words(5)) == [words(5)]


def test_predict_short_text_skips_map_reduce(monkeypatch):
    pipe = make_pipeline(monkeypatch=monkeypatch)
    calls = []
    pipe._summarize = lambda texts: calls.append(texts) or ["summary"] * len(texts)

    assert pipe.predict(words(5)) == "summary"
    assert len(calls) == 1


def test_predict_long_text_maps_then_reduces(monkeypatch):
    pipe = make_pipeline(max_tokens=10, overlap=3, monkeypatch=monkeypatch)
    calls = []

    def fake_summarize(texts):
        calls.append(len(texts))
        return ["short summary"] * len(texts)

    pipe._summarize = fake_summarize
    assert pipe.predict(words(40)) == "short summary"
    assert calls[0] > 1  # map over several chunks
    assert calls[-1] == 1  # final reduce
