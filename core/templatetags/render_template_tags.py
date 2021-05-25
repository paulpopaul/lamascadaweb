from django import template
from django.utils.safestring import mark_safe

from core.models import Category, Item
from django.db.models import Count

register = template.Library()



@register.simple_tag
def item_counter():
    item = Item.objects.filter(is_active=True)
    prod_no = item.count()
    return prod_no



@register.simple_tag
def categories():
    items = Category.objects.filter(is_active=True).order_by('title')
    items_li = ""
    for i in items:
        items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    return mark_safe(items_li)



@register.simple_tag
def categories_mobile():
    items = Category.objects.filter(is_active=True).order_by('title')
    items_li = ""
    for i in items:
        items_li += """<li class="item-menu-mobile"><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    return mark_safe(items_li)


'''

@register.simple_tag
def categories_li_a():
    items = Category.objects.filter(is_active=True).order_by('title')
    items_li_a = ""
    item_div_list = ""

    items1 = Item.objects.filter(is_active=True).annotate(count=Count('title'))
    items1_li_a = ""
    items1_li_a = """<span class="badge badge-danger badge-pill">{}</span>""".format(items1.count)
    return mark_safe(items1_li_a)

    for i in items:
        items_li_a += """<p class="mb-2"><a href="/category/{}" class="card-link-secondary">{}</a>""" + items1_li_a + """</p>""".format(i.slug, i.title)

    return mark_safe(items_li_a)

        items_li_a += """<li class="mb-1"><a href="/category/{}" class="d-flex"><span>{}</span> <span class=" ml-auto"></span><span class="badge badge-danger badge-pill">{}</span></a></li>""".format(i.slug,


'''

@register.simple_tag
def categories_li_a():
    items = Category.objects.filter(is_active=True).order_by('title').annotate(count=Count('item'))
    items_li_a = ""
    for i in items: 

        items_li_a += """ <a href="/category/{}" class="d-flex mb-1"><span>{}</span> <span class="text-black ml-auto"><span class="badge badge-primary badge-pill">{}</span></span></a>""".format(i.slug,
                                                                                                         i.title, i.count)                                                             
    return mark_safe(items_li_a)

@register.simple_tag
def categories_div():
    """
    section banner
    :return:
    """
    items = Category.objects.filter(is_active=True).order_by('title')
    items_div = ""
    item_div_list = ""
    for i, j in enumerate(items):
        if not i % 2:
            items_div += """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                j.image, j.slug, j.title)
        else:
            items_div_ = """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                j.image, j.slug, j.title)
            item_div_list += """<div class="col-sm-10 col-md-8 col-lg-4 m-l-r-auto">""" + items_div + items_div_ + """</div>"""
            items_div = ""

    return mark_safe(item_div_list)


