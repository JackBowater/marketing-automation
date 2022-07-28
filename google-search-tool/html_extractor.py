def html_extractor(check, check_position, end, r):
    check_start=r.text.find(check, check_position)
    html_start=check_start+len(check)
    html_stop=r.text.find(end, html_start)
    return r.text[html_start:html_stop], html_stop

def email_formatter(first, last, email):
    if last and email:
        f = first[0].lower()
        l = last[0].lower()
        if not email.startswith('@'):
            email = email.format(first=first.lower(), last=last.lower(), f=f, l=l)
    return email