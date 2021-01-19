from django import forms

class SearchForm(forms.Form):

    q = forms.CharField(label="Question", required=True, widget=forms.TextInput(
        attrs={'placeholder':"Enter your question here", 'style':'height:100%;width:80%;'}
    ))
    accepted = forms.NullBooleanField(label="Only accepted answers", required=False)
    answers = forms.IntegerField(label="Minimum number of answers", required=False, widget=forms.NumberInput(
        attrs={'placeholder':'No. of answers'}
    ))
    body = forms.CharField(label="Body", required=False, widget=forms.TextInput(
        attrs={'placeholder':'Text to be returned in question bodies'}
    ))
    closed = forms.NullBooleanField(label="Return closed questions", required=False)
    migrated = forms.NullBooleanField(label="Return migrated questions", required=False)
    notice = forms.NullBooleanField(label="Questions with post notices", required=False)
    nottagged = forms.CharField(label="Labels to avoid", required=False, widget=forms.TextInput(
        attrs={
            'placeholder':'Enter ; separated tags'
        }
    ))
    tagged = forms.CharField(label="Labels to look for", required=False, widget=forms.TextInput(
        attrs={
            'placeholder':'Enter ; separated tags'
        }
    ))
    title = forms.CharField(label="Text that must appear in title", required=False)
    user = forms.IntegerField(label="ID of user owning questions", required=False)
    url = forms.CharField(label="URL to be contained in response", help_text="Can also contain wildcard", required=False)
    views = forms.IntegerField(label="Minimum number of views question must have", required=False)
    wiki = forms.NullBooleanField(label="Only community Wiki questions", required=False)
    # page = forms.IntegerField(label="Page No.", required=False)
    pagesize = forms.IntegerField(label="No. of results per page", required=False)
    fromdate = forms.DateField(label="From", required=False, widget=forms.SelectDateWidget())
    todate = forms.DateField(label="To", required=False, widget=forms.SelectDateWidget())
    order = forms.ChoiceField(label="Order of response", choices=[('','None'),('asc','Ascending'),('desc','Descending')], required=False)
    sort = forms.ChoiceField(label="Sort by", choices=[('','None'),('activity','Activity'),('votes','Votes'),('creation','Creation'),('relevance','Relevance')], required=False)

# class PaginatorForm(forms.Form):

