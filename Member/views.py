from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Member
from users.models import UserProfile
from .forms import MemberForm




@login_required
def table_members(request):
    template = "members/table.html"
    members = Member.objects.filter(is_active=True)
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"members": members, "members_active_list": "active", "profile": profile}
    return render(request, template, context)



@login_required
def thumbnail_members(request):
    template = "members/thumbnail.html"
    members = Member.objects.active()
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"members": members, "members_active_list": "active","profile": profile}
    return render(request, template, context)


@login_required
def list_members(request):
    template = "members/list.html"
    members = Member.objects.active()
    profile = UserProfile.objects.get_or_create(user=request.user)
    
    member_data = []
    for member in members:
        member_info = {
            "name": member.name,
            "telephone": member.telephone,
            "location": member.location,
        }
        member_data.append(member_info)

    context = {
        "profile": profile,
        "members": member_data,
        "total": len(members),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        "total_delete": len(members),
        "status": "all",
    }
    return render(request, template, context)



@login_required
def detail_member(request, pk):
    template = "members/detail.html"
    member = get_object_or_404(Member, pk=pk)
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"member": member, "profile": profile}
    return render(request, template, context)


@login_required
def edit_member(request, pk):
    template = "members/edit.html"
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm()
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"member": member, "form": form,"profile": profile}
    return render(request, template, context)


@login_required
def update_member(request, pk):
    if request.method == "POST":
        member = get_object_or_404(Member, pk=pk)
        form = MemberForm(request.POST, request.FILES, instance=member)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.success(request, "Member Information Updated Successfully")
            return redirect("detail_member", pk=pk)
        else:
            messages.error(request, "Member Information Not Updated")
            return redirect("edit_member", pk=pk)


@login_required
def delete_member(request, pk):
    # TODO: Make this functionality available only to admins
    member = get_object_or_404(Member, pk=pk)
    member.active = False
    member.save()
    messages.success(request, "Member Deleted Successfully")
    return redirect("list_members")


@login_required
def restore_member(request, pk):
    # TODO: Make this functionality available only to admins
    member = get_object_or_404(Member, pk=pk)
    member.active = True
    member.save()
    messages.success(request, "Member Restored Successfully")
    return redirect("list_members")


@login_required
def search_members(request):
    template = "members/list.html"
    q = request.GET.get('q')
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"profile": profile}
    if q != '':
        qs = Member.objects.active().filter(
            Q(name__icontains=q) | Q(shepherd__name__icontains=q) | Q(ministry__name__icontains=q)|
            Q(location__icontains=q) | Q(fathers_name__contains=q) | Q(mothers_name__contains=q)
        )
        context["members"] = qs
        context['total'] = len(qs)
        return render(request, template, context)
    else:
        members = Member.objects.active()
        context['members'] = members
        context['total'] = len(members)
        return render(request, template, context)





@login_required
def filter_members(request):
    template = "members/thumbnail.html"
    initial_members = Member.objects.active()
    statuses = []
    for i in request.GET:
        if request.GET.get(i) == 'on':
            statuses.append(i)
    for i in statuses:
        if i == 'pays_tithe':
            initial_members = initial_members.filter(pays_tithe=True)
        elif i == 'working':
            initial_members = initial_members.filter(working=True)
        elif i == 'schooling':
            initial_members = initial_members.filter(schooling=True)
        elif i == "new_believer_school":
            initial_members = initial_members.filter(new_believer_school=True)
    # import pdb; pdb.set_trace()


    context = {
        "profile": profile,
        "members": initial_members,
        "total": len(Member.objects.active()),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
    }

    for i in statuses:
        context[i] = 'checked'

    return render(request, template, context)


@login_required
def add_member(request):
    # TODO: Make This functionality available only to admins
    template = "members/add.html"
    form = MemberForm()
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"form": form,"members_active_add": "active", "profile": profile}
    return render(request, template, context)


@login_required
def create_member(request):
    # TODO: Make this functionality available only to admins
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            member = form.save(commit=False)
            member.active = True
            member.save()
            messages.success(request, "Church Member Added Successfully")
            return redirect("list_members")
        else:
            messages.error(request, "Church Member Creation Failed")
            return redirect('add_member')


@login_required


# ================================================================================= #
#                                   Api View Functions                              #
# ================================================================================= #


def api_create_member(request, user_id):
    data = {}
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
        except:
            user = None
        if user is not None:
            if request.method == "POST":
                form = MemberForm(request.POST, request.FILES or None)
                if form.is_valid():
                    member = form.save(commit=False)
                    member.save()
                    data = {"STATUS": "OK", "MEMBER_ID": member.pk}
                    return JsonResponse(data, content_type="Application/json", safe=False)
                else:
                    data = {"STATUS": "INVALID"}
        else:
            data = {"STATUS": "INVALID", "ERROR_TYPE": "AUTHENTICATION PROBLEM", "STATUS_CODE": -1}
    else:
        data = {"STATUS": "INVALID", "ERROR_TYPE": "USER NOT LOGGED IN", "STATUS_CODE": 0}

    return JsonResponse(data, content_type="Application/json", safe=False)


