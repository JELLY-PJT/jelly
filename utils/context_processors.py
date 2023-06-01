from groups.forms import GroupForm

def get_group_form(request):
    group_form = GroupForm()
    return {'group_form': group_form}