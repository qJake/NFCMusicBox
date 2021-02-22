def select_tag_index(tags, uid):
    return next((ix for ix, x in enumerate(tags) if x['uid'] == uid), None)

def select_tag(tags, uid):
    return next((x for x in tags if x['uid'] == uid), None)
