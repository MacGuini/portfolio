from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = [
            'author',
            'username',
            'fname',
            'lname',
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'id':'title', 'class':'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder':'Write your subject here...'})
        self.fields['body'].widget.attrs.update({'id':'content','class':'block w-full text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder':'Write your post here...'})


class CommentForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class':'input block p-2.5 w-full text-sm rounded-lg border bg-gradient-to-t from-slate-700 to-blue-950 border-slate-600 placeholder-slate-400 text-cyan-200 focus:ring-blue-500 focus:border-blue-500 relative'})
