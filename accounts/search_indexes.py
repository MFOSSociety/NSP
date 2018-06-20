import datetime
from haystack import indexes
from accounts.models import ProjectDetail


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='mentor_name')
    pub_date = indexes.DateTimeField(model_attr='start_date')

    def get_model(self):
        return ProjectDetail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(start_date=datetime.datetime.now())