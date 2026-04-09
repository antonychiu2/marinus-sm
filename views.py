from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import (
    login,
    sql_lab_table
)


def sql(request):
    if request.user.is_authenticated:

        return render(request, "Lab/SQL/sql.html")
    else:
        return redirect("login")


def sql_lab(request):
    if request.user.is_authenticated:

        name = request.POST.get("name")

        password = request.POST.get("pass")

        if name:

            if login.objects.filter(user=name):

                sql_query = (
                    "SELECT * FROM introduction_login WHERE user='"
                    + name
                    + "'AND password='"
                    + password
                    + "'"
                )
                print(sql_query)
                try:
                    print("\nin try\n")
                    val = login.objects.raw(sql_query)
                except:
                    print("\nin except\n")
                    return render(
                        request,
                        "Lab/SQL/sql_lab.html",
                        {"wrongpass": password, "sql_error": sql_query},
                    )

                if val:
                    user = val[0].user
                    return render(request, "Lab/SQL/sql_lab.html", {"user1": user})
                else:
                    return render(
                        request,
                        "Lab/SQL/sql_lab.html",
                        {"wrongpass": password, "sql_error": sql_query},
                    )
            else:
                return render(request, "Lab/SQL/sql_lab.html", {"no": "User not found"})
        else:
            return render(request, "Lab/SQL/sql_lab.html")
    else:
        return redirect("login")


@csrf_exempt
def injection(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "Lab_2021/A3_Injection/injection.html")


@csrf_exempt
def injection_sql_lab(request):
    if request.user.is_authenticated:

        name = request.POST.get("name")
        password = request.POST.get("pass")
        print(name)
        print(password)

        if name:
            sql_query = (
                "SELECT * FROM introduction_sql_lab_table WHERE id='"
                + name
                + "'AND password='"
                + password
                + "'"
            )

            sql_instance = sql_lab_table(
                id="admin", password="65079b006e85a7e798abecb99e47c154"
            )
            sql_instance.save()
            sql_instance = sql_lab_table(id="jack", password="jack")
            sql_instance.save()
            sql_instance = sql_lab_table(
                id="slinky", password="b4f945433ea4c369c12741f62a23ccc0"
            )
            sql_instance.save()
            sql_instance = sql_lab_table(
                id="bloke", password="f8d1ce191319ea8f4d1d26e65e130dd5"
            )
            sql_instance.save()

            print(sql_query)

            try:
                user = sql_lab_table.objects.raw(sql_query)
                user = user[0].id
                print(user)

            except:
                return render(
                    request,
                    "Lab_2021/A3_Injection/sql_lab.html",
                    {"wrongpass": password, "sql_error": sql_query},
                )

            if user:
                return render(
                    request, "Lab_2021/A3_Injection/sql_lab.html", {"user1": user}
                )
            else:
                return render(
                    request,
                    "Lab_2021/A3_Injection/sql_lab.html",
                    {"wrongpass": password, "sql_error": sql_query},
                )
        else:
            return render(request, "Lab_2021/A3_Injection/sql_lab.html")
    else:
        return redirect("login")
