import ast
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
import os
from django.conf import settings
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.core.paginator import Paginator
import csv
import pandas as pd
from keplergl import KeplerGl
import datetime
from django.contrib import messages


def Home(request):
    messages.success(request, "Welcome to Kepler Command Center.")
    return render(request, "home.html")


@login_required(login_url="login")
def FileUploader(request):
    form = FileForm()
    if request.method == "POST":

        mydata = FileForm(request.POST, request.FILES)
        if mydata.is_valid():

            x = mydata.save(commit=False)

            x.user_name = request.user
            x.save(request.FILES["file"])
            messages.success(request, "File Uploaded")

            return redirect("table")
    context = {"form": form}
    return render(request, "index.html", context)


@login_required(login_url="login")
def CovertedToDB_list(request):

    queryset = CovertedToDB.objects.filter(user_name=request.user)
    date = request.GET.get("filterdate")
    city = request.GET.get("city")
    circle = request.GET.get("circle")
    component = request.GET.get("component")

    page = request.GET.get("page")

    if date:
        request.session["filterdate"] = date
    elif page is not None:
        date = request.session.get("filterdate")

    if city:
        request.session["city"] = city
    elif page is not None:
        city = request.session.get("city")

    if circle:
        request.session["circle"] = circle
    elif page is not None:
        circle = request.session.get("circle")

    if component:
        request.session["component"] = component
    elif page is not None:
        component = request.session.get("component")

    if city and date:
        queryset = queryset.filter(City__icontains=city, Monitering_Date=date)
    if circle and date:
        queryset = queryset.filter(Circle__icontains=circle, Monitering_Date=date)
    if component and date:
        queryset = queryset.filter(Component__icontains=component, Monitering_Date=date)
    if city and circle and component and date:
        queryset = queryset.filter(
            City__icontains=city,
            Circle__icontains=circle,
            Component__icontains=component,
            Monitering_Date=date,
        )
    elif city and circle and date:
        queryset = queryset.filter(
            City__icontains=city, Circle__icontains=circle, Monitering_Date=date
        )
    elif city and component and date:
        queryset = queryset.filter(
            City__icontains=city, Component__icontains=component, Monitering_Date=date
        )
    elif circle and component and date:
        queryset = queryset.filter(
            Circle__icontains=circle,
            Component__icontains=component,
            Monitering_Date=date,
        )

    paginator = Paginator(queryset, 5)
    venues = paginator.get_page(page)

    search = request.GET.get("searchbutton")
    generate = request.GET.get("generatebutton")
    delete = request.GET.get("deletebutton")
    reset = request.GET.get("resetbutton")

    if generate:
        messages.success(request, "Filtered Data Sucessfully.")

        data = list(queryset.values())
        df = pd.DataFrame(data)
        # print(df.columns.unique())

        showtime = datetime.datetime.now().strftime("%Y_%m_%d[%H_%M_%S]")

        merge_df = df.loc[
            :,
            [
                "Circle",
                "City",
                "Component",
                "Date",
                "Hour",
                "Total_Customers",
                "Anomaly",
                "Ratio_Data",
                "Ratio_Voice",
                "Ratio_HSI",
                "cluster_issue",
                "Data_Volume",
                "Data_Volume_Formula",
                "Data_Volume_mean",
                "Data_Volume_std",
                "Voice_Affected_Users",
                "Voice_Affected_Users_Formula",
                "Voice_Affected_Users_mean",
                "Voice_Affected_Users_std",
                "HSI_Affected_Users",
                "HSI_Affected_Users_Formula",
                "HSI_Affected_Users_mean",
                "HSI_Affected_Users_std",
                "Data_Change",
                "Voice_Change",
                "HSI_Change",
                "num_grids",
                "num_cells",
                "num_sectors",
                "Indoor_Freqency_850",
                "Indoor_Freqency_1800",
                "Indoor_Freqency_2300",
                "prb_20",
                "prb_70_90",
                "prb_90",
                "prb_20_per",
                "prb_70_90_per",
                "prb_90_per",
                "area",
                "month",
                "week",
                "total_users_data_complaints",
                "total_users_vvm_complaints",
                "total_users_covergae_complaints",
                "total_users_other_complaints",
                "total_upc_generated",
                "Polygon",
            ],
        ]


        # creating point df for kepler
        point_df = df.loc[
            :, ["Circle", "City", "Component", "Polygon"]
        ].drop_duplicates()
        point_df["point"] = point_df["Polygon"].apply(
            lambda x: eval(x)["coordinates"][0]
        )
        point_df = point_df.explode("point")
        point_df["lat"] = point_df["point"].apply(lambda x: x[1])
        point_df["lon"] = point_df["point"].apply(lambda x: x[0])
        # minlat=point_df['lat'].min()
        # maxlat=point_df['lat'].max()
        avglat = point_df["lat"].mean()
        avglon = point_df["lon"].mean()
        # minlon=point_df['lon'].min()
        # maxlon=point_df['lon'].max()
        print(avglat)
        print(avglon)
        # min lat max lat, get avg
        # min long max long get avg
        map_yt = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [],
                    "layers": [
                        {
                            "id": "4lrj2t8",
                            "type": "geojson",
                            "config": {
                                "dataId": "Data",
                                "label": "Data",
                                "color": [18, 147, 154],
                                "columns": {"geojson": "Polygon"},
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "strokeOpacity": 0.8,
                                    "thickness": 0.5,
                                    "strokeColor": [255, 203, 153],
                                    "colorRange": {
                                        "name": "Uber Viz Diverging 1.5",
                                        "type": "diverging",
                                        "category": "Uber",
                                        "colors": [
                                            "#00939C",
                                            "#5DBABF",
                                            "#BAE1E2",
                                            "#F8C0AA",
                                            "#DD7755",
                                            "#C22E00",
                                        ],
                                    },
                                    "strokeColorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "radius": 10,
                                    "sizeRange": [0, 10],
                                    "radiusRange": [0, 50],
                                    "heightRange": [0, 500],
                                    "elevationScale": 5,
                                    "enableElevationZoomFactor": True,
                                    "stroked": False,
                                    "filled": True,
                                    "enable3d": False,
                                    "wireframe": False,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {
                                "colorField": {
                                    "name": "Voice_Affected_Users",
                                    "type": "integer",
                                },
                                "colorScale": "quantile",
                                "strokeColorField": None,
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear",
                            },
                        },
                        {
                            "id": "zy1dtyk",
                            "type": "point",
                            "config": {
                                "dataId": "Point",
                                "label": "Point",
                                "color": [25, 20, 16],
                                "columns": {
                                    "lat": "lat",
                                    "lng": "lon",
                                    "altitude": None,
                                },
                                "isVisible": True,
                                "visConfig": {
                                    "radius": 12.9,
                                    "fixedRadius": False,
                                    "opacity": 0.8,
                                    "outline": False,
                                    "thickness": 2,
                                    "strokeColor": None,
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "strokeColorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "radiusRange": [0, 50],
                                    "filled": True,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {
                                "colorField": None,
                                "colorScale": "quantile",
                                "strokeColorField": None,
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                            },
                        },
                    ],
                    "interactionConfig": {
                        "tooltip": {
                            "fieldsToShow": {
                                "Data": [
                                    {"name": "Circle", "format": None},
                                    {"name": "City", "format": None},
                                    {"name": "Component", "format": None},
                                    {"name": "Date", "format": None},
                                    {"name": "Hour", "format": None},
                                ],
                                "Point": [
                                    {"name": "Component", "format": None},
                                    {"name": "Circle", "format": None},
                                    {"name": "City", "format": None},
                                ],
                            },
                            "compareMode": False,
                            "compareType": "absolute",
                            "enabled": True,
                        },
                        "brush": {"size": 0.5, "enabled": False},
                        "geocoder": {"enabled": False},
                        "coordinate": {"enabled": False},
                    },
                    "layerBlending": "normal",
                    "splitMaps": [],
                    "animationConfig": {"currentTime": None, "speed": 1},
                },
                "mapState": {
                    "bearing": 0,
                    "dragRotate": False,
                    "latitude": avglat,
                    "longitude": avglon,
                    "pitch": 0,
                    "zoom": 6,
                    "isSplit": False,
                },
                "mapStyle": {
                    "styleType": "light",
                    "topLayerGroups": {},
                    "visibleLayerGroups": {
                        "label": True,
                        "road": True,
                        "border": False,
                        "building": True,
                        "water": True,
                        "land": True,
                        "3d building": False,
                    },
                    "threeDBuildingColor": [
                        218.82023004728686,
                        223.47597962276103,
                        223.47597962276103,
                    ],
                    "mapStyles": {},
                },
            },
        }
        point_df.drop(["Polygon", "point"], inplace=True, axis=1)
        

        map_dual = KeplerGl(height=700)
        map_dual.save_to_html(
            data={"Data": merge_df, "Point": point_df},
            file_name=f"media/Kepler_{showtime}.html",
            config=map_yt,
        )
        messages.success(request, "Kepler file generated. View File Explorer")

        file = f"Kepler_{showtime}.html"
        file_path = os.path.basename(file)
        fileupload = Upload.objects.create(user_name=request.user, file=file_path)
        fileupload.save()

        context = {"venues": venues}
        return render(request, "filter.html", context)

    elif reset:
        queryset = CovertedToDB.objects.filter(user_name=request.user)
        request.session.pop("filterdate", None)
        request.session.pop("circle", None)
        request.session.pop("city", None)
        request.session.pop("component", None)
        return redirect("dblist")

    elif delete:
        data = CovertedToDB.objects.filter(user_name=request.user).delete()
        messages.success(request, "DB is deleted!")
        context = {"venues": venues}
        return render(request, "filter.html", context)

    elif search:
        messages.success(request, "Filtered Data Sucessfully.")
        context = {"venues": venues}
        return render(request, "filter.html", context)
    else:
        context = {"venues": venues}
        return render(request, "filter.html", context)


@login_required(login_url="login")
def csvconverter(request):
    messages.success(request, "Please Upload the Monitoring Report(format:csv).")

    form = CsvForm()
    if request.method == "POST":

        mydata = CsvForm(request.POST, request.FILES)

        if mydata.is_valid():

            x = mydata.save(commit=False)
            x.user_name = request.user
            csv_file = request.FILES["file"]
            print(csv_file)
            x.save(csv_file)

            user_name = request.user
            file = csv_file
            upload = Upload.objects.create(user_name=user_name, file=file)
            upload.save()

            obj = Csv.objects.get(activated=False)
            # date_file=Csv.objects.filter(user_name=x.user_name,file=x.file)
            # print(date_file)

            with open(obj.file.path, "r") as f:

                # messages.success(request,"File is Converting.")
                reader = csv.reader(f, delimiter=",")
                # reader=pd.read_csv(f)
                next(reader)
                batch_size = 20000
                objs = []

                for fields in reader:
                    # if CovertedToDB.objects.filter(Circle=fields[0]).exists() and CovertedToDB.objects.filter(City=fields[1]).exists() and CovertedToDB.objects.filter(Component=fields[2]).exists() and CovertedToDB.objects.filter(lat=fields[45]).exists() and CovertedToDB.objects.filter(lon=fields[46]).exists():
                    #     messages.error(request, "Data already exists")
                    # continue
                    # else:
                    objs.append(
                        CovertedToDB(
                            Monitering_Date=obj.date,
                            user_name=request.user,
                            Circle=fields[0],
                            City=fields[1],
                            Component=fields[2],
                            Date=fields[3],
                            Hour=fields[4],
                            Total_Customers=fields[5],
                            Anomaly=fields[6],
                            Ratio_Data=fields[7],
                            Ratio_Voice=fields[8],
                            Ratio_HSI=fields[9],
                            cluster_issue=fields[10],
                            Data_Volume=fields[11],
                            Data_Volume_Formula=fields[12],
                            Data_Volume_mean=fields[13],
                            Data_Volume_std=fields[14],
                            Voice_Affected_Users=fields[15],
                            Voice_Affected_Users_Formula=fields[16],
                            Voice_Affected_Users_mean=fields[17],
                            Voice_Affected_Users_std=fields[18],
                            HSI_Affected_Users=fields[19],
                            HSI_Affected_Users_Formula=fields[20],
                            HSI_Affected_Users_mean=fields[21],
                            HSI_Affected_Users_std=fields[22],
                            Data_Change=fields[23],
                            Voice_Change=fields[24],
                            HSI_Change=fields[25],
                            num_grids=fields[26],
                            num_cells=fields[27],
                            num_sectors=fields[28],
                            Indoor_Freqency_850=fields[29],
                            Indoor_Freqency_1800=fields[30],
                            Indoor_Freqency_2300=fields[31],
                            prb_20=fields[32],
                            prb_70_90=fields[33],
                            prb_90=fields[34],
                            prb_20_per=fields[35],
                            prb_70_90_per=fields[36],
                            prb_90_per=fields[37],
                            area=fields[38],
                            month=fields[39],
                            week=fields[40],
                            total_users_data_complaints=fields[41],
                            total_users_vvm_complaints=fields[42],
                            total_users_covergae_complaints=fields[43],
                            total_users_other_complaints=fields[44],
                            total_upc_generated=fields[45],
                            Polygon=fields[46],
                        )
                    )

                    # Insert data in batches
                    if len(objs) == batch_size:
                        CovertedToDB.objects.bulk_create(objs)
                        objs = []
                # for i,fields in enumerate(reader):
                #     if i==0:
                #         pass
                #     elif CovertedToDB.objects.filter(Circle=fields[0]).exists() and CovertedToDB.objects.filter(City=fields[1]).exists() and CovertedToDB.objects.filter(Component=fields[2]).exists() and CovertedToDB.objects.filter(lat=fields[47]).exists() and CovertedToDB.objects.filter(lon=fields[48]).exists():
                #         messages.error(request,"Data Exists Alredy")
                #         continue

                #     else:
                #         objs=[CovertedToDB(Monitering_Date=obj.date,user_name=request.user,Circle=fields[0],City=fields[1],Component=fields[2],Date=fields[3],Hour=fields[4],
                #             Total_Customers=fields[5],Anomaly=fields[6],Ratio_Data=fields[7],Ratio_Voice=fields[8],
                #             Ratio_HSI=fields[9],cluster_issue=fields[10],Data_Volume=fields[11],Data_Volume_Formula=fields[12],
                #             Data_Volume_mean=fields[13],Data_Volume_std=fields[14],Voice_Affected_Users=fields[15],
                #             Voice_Affected_Users_Formula=fields[16],
                #             Voice_Affected_Users_mean=fields[17],Voice_Affected_Users_std=fields[18],
                #             HSI_Affected_Users=fields[19],HSI_Affected_Users_Formula=fields[20],HSI_Affected_Users_mean=fields[21],
                #             HSI_Affected_Users_std=fields[22],Data_Change=fields[23],Voice_Change=fields[24],HSI_Change=fields[25],
                #             num_grids=fields[26],num_cells=fields[27],num_sectors=fields[28],Indoor_Freqency_850=fields[29],
                #             Indoor_Freqency_1800=fields[30],Indoor_Freqency_2300=fields[31],prb_20=fields[32],prb_70_90=fields[33],
                #             prb_90=fields[34],prb_20_per=fields[35],prb_70_90_per=fields[36],prb_90_per=fields[37],
                #             area=fields[38],month=fields[39],week=fields[40],total_users_data_complaints=fields[41],total_users_vvm_complaints=fields[42] ,
                #             total_users_covergae_complaints=fields[43],total_users_other_complaints=fields[44],total_upc_generated=fields[45],
                #             Polygon=fields[46]
                #         )]

                #         CovertedToDB.objects.bulk_create(objs)

                obj.activated = True
                obj.save()
                messages.success(
                    request, "Csv converted to DB! Visit at Search through DB"
                )
            myfile = obj.file.path
            print(myfile)
            if os.path.exists(myfile):
                os.remove(myfile)

    context = {"form": form}

    return render(request, "csvfeature.html", context)


@login_required(login_url="login")
def table(request):
    messages.success(request, "Look at whats been uploaded.")

    try:
        public = Upload.objects.filter(public=True)
        upload = Upload.objects.filter(user_name=request.user)
        context = {"public": public, "upload": upload}
    except:
        context = {"public": "None", "upload": "None"}
    return render(request, "table.html", context)


@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html")


def signuppage(request):
    if request.method == "POST":
        user = request.POST["Name"]
        e_mail = request.POST["email"]
        password1 = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]

        if password1 == confirmpassword:
            if not User.objects.filter(username=user).exists():

                if not User.objects.filter(email=e_mail).exists():

                    user = User.objects.create_user(
                        username=user, email=e_mail, password=password1
                    )
                    user.save()
                    messages.success(request, "Account Created!")
        return redirect("login")
    return render(request, "signup.html")


def loginpage(request):
    if request.method == "POST":
        username = request.POST["Name"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # pruser)
            login(request, user)
            return redirect("home")
        # premail,password)
        else:
            messages.error(request, "Error please check your credentials!")
            return redirect("login")
    else:
        return render(request, "login.html")


@login_required(login_url="login")
def logoutpage(request):
    # pr"logout")
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def updatefiles(request, id):

    data = Upload.objects.get(id=id)
    updateform = FileForm(request.POST or None, instance=data)
    if updateform.is_valid():
        updateform.save()
        messages.success(request, "File Status is Updated!")
        return redirect("table")
    context = {"form": updateform}
    return render(request, "update.html", context)


@login_required(login_url="login")
def deletefiles(request, id):
    data = Upload.objects.get(id=id)
    myfile = str(data.file.path)
    if os.path.exists(myfile):
        os.remove(myfile)
        data.delete()
        messages.success(request, "File is Deleted!")
        return redirect("table")
    else:
        print("files does not exists")
        messages.error(request, "File is Not Deleted!")
        return redirect("table")
