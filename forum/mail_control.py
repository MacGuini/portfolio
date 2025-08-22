from django.core.mail import EmailMessage

def commentReplied(comment):
    # Common variables used in both notifications
    pageId = comment.post.id
    url = f"https://brian-lindsay.com/forum/view-post/{pageId}"
    from_email = "noreply@brian-lindsay.com"

    # Notify when someone replies to another user's comment
    if comment.parent is not None and comment.author != comment.parent.author:
        subject = f"Hello, {comment.parent.fname}! {comment.username} replied to your comment at brian-lindsay.com!"
        to = [comment.parent.author.email]
        content = f"""
        <p>{comment.username} has replied to a comment you made at <a href='https://brian-lindsay.com'>brian-lindsay.com</a>.</p>
        <p>{comment.username} said, "{comment.text}" to your comment, "{comment.parent.text}" on a forum post titled {comment.post.title}.</p>
        <p><a href="{url}">Click here to view the post</a></p>
        <p>If you are unable to click the link, copy and paste the URL below into your browser.<br>{url}</p>
        <p>Always remember to check and verify the email being sent to you. For more information, visit brian-lindsay.com or contact Brian Lindsay directly to verify.</p>
        """
        
    # Notify when someone comments on another user's post
    elif comment.author != comment.post.author:
        subject = f'Hello, {comment.post.author.fname}! {comment.username} made a comment on your post at brian-lindsay.com!'
        to = [comment.post.author.email]
        content = f"""
        <p>{comment.username} has made a comment on your post titled "{comment.post.title}" saying, "{comment.text}"</p>
        <p><a href="{url}">Click here to view the post</a></p>
        <p>If you are unable to click the link, copy and paste the URL below into your browser.<br>{url}</p>
        <p>Always remember to check and verify the email being sent to you. For more information, visit brian-lindsay.com or contact Brian Lindsay directly to verify.</p>
        """

    # Send the email if 'to' is set (meaning one of the conditions was met)
    if 'to' in locals():
        email = EmailMessage(
            subject=subject,
            body=content,
            from_email=from_email,
            to=to,
        )
        email.content_subtype = "html"
        email.send()
