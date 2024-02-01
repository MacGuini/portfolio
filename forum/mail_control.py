from django.core.mail import EmailMessage

def commentReplied(comment):
    pageId = comment.post.id
    url = f"https://brian-lindsay.com/forum/view-post/{pageId}"
    subject = f"Hello, {comment.parent.fname}! {comment.username} replied to your comment on brian-lindsay.com!"
    from_email = "brian.s.lindsay829@gmail.com"
    to = [comment.parent.author.email]
    content = f"""
    <p>{comment.username} has replied to a comment you made at <a href='https://brian-lindsay.com'>brian-lindsay.com</a>.</p>
    <p>{comment.username} said, "{comment.text}" to your comment, "{comment.parent.text}" on a forum post titled {comment.post.title}.</p>
    <p><a href="{url}">Click here to view the post</a></p>
    <p>If you are unable to click the link, copy and paste the URL below into your browser.<br>{url}</p>
    <p>Always remember to check and verify the email being sent to you. For more information, visit brian-lindsay.com or contact Brian Lindsay directly to verify.</p>
    """
    
    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_email,
        to=to,
    )
    email.content_subtype = "html"
    email.send()

