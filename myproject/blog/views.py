from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.





def home(request):
    return render(request, 'blog/home.html')

def test(request):
    return render(request, 'blog/test.html')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    return render(request, 'blog/dashboard.html')


def userlogin(request):
    if request.method == "POST":
        print("userlogin post")
        fm = AuthenticationForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            password = fm.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if user.profile.type == "buyer":
                    return redirect('buyerprofile',id=request.user.id)
                elif user.profile.type == "seller":
                    return redirect('sellerprofile', id = request.user.id)
                elif user.profile.type == "admin":
                    return redirect('adminprofile', id = request.user.id)
            else:
                print("user not found")
                fm = AuthenticationForm()
                return render(request, 'blog/userlogin.html', {"form": fm})   

    else:
        fm = AuthenticationForm()
        return render(request, 'blog/userlogin.html', {"form": fm})

        
    return render(request, 'blog/userlogin.html')


from django.contrib.auth import logout


def logoutview(request):
    # Log out the user
    logout(request)
    
    # Redirect to a specific page (optional)
    return redirect('userlogin')




from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            type_data = form.cleaned_data.get('type')
            user.profile.type = type_data
            user.save()
            #raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)

            
            return redirect('userlogin')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def buyerprofile(request,id):
    
    return render(request, 'blog/buyerprofile.html')# starts from website address

def buyerupload(request):
    if request.method == 'POST':
        print("hello world")
        name = request.POST.get('name')
        print(name)
    else:
        return render(request, 'blog/buyerupload.html')# starts from website address
    return render(request, 'blog/buyerupload.html')# starts from website address


def buyersearch(request):
    if request.method == 'POST':
        searchinput = request.POST.get("searchInput")
        
        print("searchinput")
        print(searchinput)

        productresult=[]
        priceresult=[]


       
        from django.db import connection

        # Previously it was searched with ILIKE
        # sql_query = """
        #     SELECT * FROM productdetail
        #     WHERE productname ILIKE %s
        # """


        # Currently using full_text_search using 

        # sql_query = """
        #         SELECT * FROM productdetail
        #         WHERE to_tsvector('english', productname) @@ to_tsquery('english', %s)
        # """

        # Provide the parameter value
        search_text = request.POST.get("searchInput")


        # sql_query= '''SELECT *
        #             FROM your_table
        #             WHERE to_tsvector('english', your_column) @@ to_tsquery('english', 'your_pattern');
        #             '''


        sql_query = """
                SELECT * FROM productdetail
                WHERE to_tsvector('english', productname) @@ to_tsquery('english', %s)
        """

        # Execute the raw SQL query with a prepared statement
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [f'%{search_text}%'])
            productresult = cursor.fetchall()
            print("Search Results")
            print(productresult)

        # from django.db import connection
        # with connection.cursor() as cursor:
        #     # Write your raw SQL insert statement ILIKE '%your_text%'SELECT * FROM your_table
        #     #WHERE your_column ILIKE '%your_text%';
        #     cursor.execute('SELECT * FROM productdetail WHERE productname ILIKE %s', (searchinput,))
        #     productresult = cursor.fetchall()

        

        #     tempresult=[]
            for r in productresult:
                print(r[0])
                cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
                priceresult.append(cursor.fetchone())
                
                
            connection.commit()
        print()    
        print(priceresult)
    
        mylist = zip(productresult, priceresult)
        
       

            
            



        print("result")
        print(productresult)
        print(priceresult)
        return render(request, 'blog/buyersearchresult.html', {"mylist": mylist})

            

       
    else:
        return render(request, 'blog/buyersearch.html')# starts from website address
    return render(request, 'blog/buyersearch.html')# starts from website address



def buyerbookmarklist(request):
    productresult=[]
    priceresult=[]


    from django.db import connection

    sql_query='''
            SELECT *
            FROM bookmarklist
            JOIN productdetail 
            ON bookmarklist.productid = productdetail.productdetailid
            WHERE bookmarklist.customerid = %s
            ;  
            '''



    # Provide the parameter value
    search_text = request.POST.get("searchInput")

    # Execute the raw SQL query with a prepared statement
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [request.user.id,])
        productresult = cursor.fetchall()

    return render(request, 'blog/buyerbookmarklist.html', {"productresult": productresult })




    # Provide the parameter value
    # search_text = request.POST.get("searchInput")

    # Execute the raw SQL query with a prepared statement
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [request.user.id,])
        productresult = cursor.fetchall()

    print(productresult)
    return render(request, 'blog/buyerbookmarklist.html', {"productresult": productresult })


def buyermessagelist(request,id):
    productresult=[]
    priceresult=[]


    from django.db import connection

    sql_query='''SELECT pricealert.productid,pricetoalert,price,pricehistory.date
            FROM pricealert
            JOIN pricehistory ON pricealert.productid = pricehistory.productid
            WHERE pricealert.buyerid = %s
            AND pricehistory.price <= pricealert.pricetoalert
            AND pricehistory.date > pricealert.date
            ;  
            '''



    # Provide the parameter value
    search_text = request.POST.get("searchInput")

    # Execute the raw SQL query with a prepared statement
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [id,])
        productresult = cursor.fetchall()

    return render(request, 'blog/buyermessagelist.html',{"productresult": productresult })

def sellerproductlist(request):
    if request.method == 'GET':
        searchinput = request.POST.get("searchInput")
        
        print("sellerproductlist")
        productresult=[]
        priceresult=[]
        tempresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE merchantid=%s', (request.user.id,))
            productresult = cursor.fetchall()

        

            
            for r in productresult:
                print(r[0])
                cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
                priceresult.append(cursor.fetchone())
                #priceresult = priceresult + tempresult
                
            connection.commit()
        print()    
        print(tempresult)
    
        mylist = zip(productresult, priceresult)
        
       

            
            



        print("result")
        print(productresult)
        print(tempresult)

        return render(request, 'blog/sellerproductlist.html', {"mylist": mylist})

            

       
    else:
        return render(request, 'blog/sellerproductlist.html')# starts from website address
    
    return render(request, 'blog/sellerproductlist.html')# starts from website address


def buyerproductdetail(request, id):
    if request.method == 'GET':
        searchinput = request.GET.get("searchInput")

        productresult=[]
        priceresult=[]
        

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            productresult = cursor.fetchall()

        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult.append(cursor.fetchone())

            

            connection.commit()
            # for r in productresult:
            #     print(r[0])
            #     cursor.execute('SELECT * FROM pricehistory WHERE productid=%s', (r[0],))
            #     tempresult = cursor.fetchall()
            #     priceresult = priceresult + tempresult
                

        # print()    
        # print(priceresult)
    
        # mylist = zip(productresult, priceresult)
        
       

            
        
        print("result")
        print(productresult)
        print(priceresult)
        return render(request, 'blog/buyerproductdetail.html', {"productresult": productresult, "priceresult": priceresult})


def buyerproductdetailpricehistory(request,id):
    if request.method == "GET":
        productresult=[]
        priceresult=[]
        minresult = 0

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            productresult = cursor.fetchall()

        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult = cursor.fetchall()

            

            sql_query_2 = '''
                SELECT MIN(price) AS min_value
                FROM pricehistory
                WHERE productid=%s;
            '''

            # Execute the query with prepared statements
            cursor.execute(sql_query_2, (id,))

            # Fetch the results
            minresult = cursor.fetchall()

            connection.commit()
            print("price history")
            print(priceresult)

        return render(request, 'blog/buyerproductdetailpricehistory.html', {"priceresult": priceresult,"minresult": minresult})
    
    elif request.method == "POST":
        print("")
        print(id)


        filterinput = request.POST.get("filterinput")

        if(filterinput == ''):
            filterinput = 0
        
        else:
            filterinput = int(filterinput)
            

        print("days")
        print(filterinput)
        
        productresult=[]
        priceresult=[]
        minresult = 0

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            #cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            #productresult = cursor.fetchall()

        
            from datetime import datetime, timedelta


            # Specify the datetime range
            start_datetime = datetime.now() - timedelta(days= filterinput)
            if(filterinput == ''):
                start_datetime = 0
            end_datetime = datetime.now()

            # SQL query with a datetime range
            sql_query = """
                SELECT *
                FROM pricehistory
                WHERE date BETWEEN %s AND %s
                AND productid=%s;
            """

            # Execute the query with prepared statements
            cursor.execute(sql_query, (start_datetime, end_datetime, id))

            # Fetch the results
            priceresult = cursor.fetchall()


            sql_query_2 = '''
                SELECT MIN(price) AS min_value
                FROM pricehistory
                WHERE date BETWEEN %s AND %s
                AND productid=%s;
            '''

            # Execute the query with prepared statements
            cursor.execute(sql_query_2, (start_datetime, end_datetime, id))

            # Fetch the results
            minresult = cursor.fetchall()


            #cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            #priceresult = cursor.fetchall()

            
            connection.commit()
            print("price history")
            print(priceresult)


            print("minprice")
            print("minresult")



        return render(request, 'blog/buyerproductdetailpricehistory.html', {"priceresult": priceresult, "minresult": minresult})
        
        

    



def sellerproductdetail(request, id):
    if request.method == 'GET':
        searchinput = request.GET.get("searchInput")

        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            productresult = cursor.fetchall()

           

            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult.append(cursor.fetchone())

            connection.commit()
            # for r in productresult:
            #     print(r[0])
            #     cursor.execute('SELECT * FROM pricehistory WHERE productid=%s', (r[0],))
            #     tempresult = cursor.fetchall()
            #     priceresult = priceresult + tempresult
                

        # print()    
        # print(priceresult)
    
        # mylist = zip(productresult, priceresult)
        
       

            
        
        print("result")
        print(productresult)
        print(priceresult)
        return render(request, 'blog/sellerproductdetail.html', {"productresult": productresult, "priceresult": priceresult})


def sellerproductdetailupdate(request, id):
    if request.method == 'GET':
        searchinput = request.GET.get("searchInput")

        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            productresult = cursor.fetchall()

        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult.append(cursor.fetchone())

            
            connection.commit()
            # for r in productresult:
            #     print(r[0])
            #     cursor.execute('SELECT * FROM pricehistory WHERE productid=%s', (r[0],))
            #     tempresult = cursor.fetchall()
            #     priceresult = priceresult + tempresult
                

        # print()    
        # print(priceresult)
    
        # mylist = zip(productresult, priceresult)
        
       

            
        
        print("result")
        print(productresult)
        print(priceresult)
        return render(request, 'blog/sellerproductdetailupdate.html', {"productresult": productresult, "priceresult": priceresult})


    elif request.method == 'POST':
        print("hello world")
        print("sellerproductdetailupdate")
        name = request.POST.get('name')
        origin = request.POST.get('origin')
        price = request.POST.get('price')
        platform = request.POST.get('platform')
        merchantid = request.user.id
        productid = id
        print(name)
        print(origin)
        print(price)
        print(platform)
        print(request.user.id)


        from django.db import connection

        



      



    # Provide the values to replace the placeholders


    # Execute the raw SQL query with prepared statements
        with connection.cursor() as cursor:
            

                
                    # Write your raw SQL insert statement
                    #fine your SQL query with placeholders (%s for PostgreSQL)
            sql_query = """
                UPDATE productdetail
                SET productname = %s,
                    productorigin = %s,
                    productplatform = %s,
                    merchantid = %s
                WHERE productdetailid = %s
                """
            params = [name, origin, platform, request.user.id, id]         


            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_query, params)
                

        


            # Commit the transaction
            connection.commit()

       
            # Write your raw SQL insert statement

            from datetime import datetime, timezone

            dt = datetime.now(timezone.utc)
            
            sql_insert = "INSERT INTO pricehistory(productid,price,date) VALUES( %s, %s, %s ) RETURNING priceid;"
            values = (id, price, dt)  # Replace with your actual values

            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_insert, values)
            



            # Commit the transaction
            connection.commit()



        # # Call the function to insert data and get the latest object
        
        from django.shortcuts import redirect
        from django.urls import reverse

        param_value = id

        # Generate the URL for the target view with the parameter
        #target_url = reverse('sellerproductdetail', kwargs={'param_id': id})

        # Perform the redirect
        return redirect('sellerproductdetail',id=id)

       

        # from django.db import connection
        # cursor = connection.cursor()
        # b = cursor.execute("INSERT INTO productdetail(productname,productorigin,productplatform,merchantid) VALUES( %s, %s, %s, %s )", [ name, origin, platform,merchantid])
    
    

def admininsights(request):
    searchinput = request.GET.get("searchInput")

    productresult=[]
    priceresult=[]

    from django.db import connection
    with connection.cursor() as cursor:
        # Write your raw SQL insert statement
        sql_query ='''
        SELECT productid,COUNT(*) AS repetition_count, productname, productorigin, productplatform
        FROM bookmarklist
        JOIN productdetail 
        ON bookmarklist.productid = productdetail.productdetailid
        GROUP BY productid,productname, productorigin, productplatform
        ORDER BY repetition_count DESC
        LIMIT 5;
        '''

        cursor.execute(sql_query, [request.user.id,])
        productresult = cursor.fetchall()
        connection.commit()

    return render(request, 'blog/admininsights.html',{"productresult": productresult})# starts from website address
    

from django.http import JsonResponse
import json

def ajaxpostforpricealert(request):
    if request.method == 'POST':
        data = request.body # Retrieve data from the POST request
        # Process the data or perform any other necessary operations
        data = json.loads(data)
        print("data from ajax")
        print(data)
        productid = data['productid']
        pricetoalert = data['pricetoalert']


        from django.db import connection

        
        last_inserted_id = 0
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            from datetime import datetime, timezone

            dt = datetime.now(timezone.utc)
            sql_insert = "INSERT INTO pricealert(buyerid,productid,pricetoalert,date) VALUES( %s, %s, %s, %s) RETURNING pricealertid;"
            values = (request.user.id, productid, pricetoalert,dt)  # Replace with your actual values

            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_insert, values)
            last_inserted_id = cursor.fetchone()[0]

            print(last_inserted_id)



            # Commit the transaction
            connection.commit()


        # Return a JSON response
        return JsonResponse({'message': 'Bookmarked successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


def ajaxpostforbookmarklist(request):
    if request.method == 'POST':
        data = request.body # Retrieve data from the POST request
        # Process the data or perform any other necessary operations
        data = json.loads(data)
        print("data from ajax")
        print(data)
        productid = data['productid']
        


        from django.db import connection

        
        last_inserted_id = 0
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            sql_insert = "INSERT INTO bookmarklist(productid, customerid) VALUES( %s, %s) RETURNING bookmarklistid;"
            values = ( productid,request.user.id)  # Replace with your actual values

            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_insert, values)
            last_inserted_id = cursor.fetchone()[0]

            print(last_inserted_id)



            # Commit the transaction
            connection.commit()


        # Return a JSON response
        return JsonResponse({'message': 'Bookmarked successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})









def sellerprofile(request,id):

    return render(request, 'blog/sellerprofile.html')# starts from website address

def sellerupload(request):
    if request.method == 'POST':
        print("hello world")
        name = request.POST.get('name')
        origin = request.POST.get('origin')
        price = request.POST.get('price')
        platform = request.POST.get('platform')
        merchantid = request.user.id
        print(name)
        print(origin)
        print(request.user.id)
        from django.db import connection

        
        last_inserted_id = 0
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            sql_insert = "INSERT INTO productdetail(productname,productorigin,productplatform,merchantid) VALUES( %s, %s, %s, %s ) RETURNING productdetailid;"
            values = (name, origin, platform,merchantid)  # Replace with your actual values

            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_insert, values)
            last_inserted_id = cursor.fetchone()[0]

            print(last_inserted_id)



            # Commit the transaction
            connection.commit()

        with connection.cursor() as cursor:
            # Write your raw SQL insert statement

            from datetime import datetime, timezone

            dt = datetime.now(timezone.utc)
            
            sql_insert = "INSERT INTO pricehistory(productid,price,date) VALUES( %s, %s, %s ) RETURNING priceid;"
            values = (last_inserted_id, price, dt)  # Replace with your actual values

            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_insert, values)
            



            # Commit the transaction
            connection.commit()



        # # Call the function to insert data and get the latest object
        
        


        # from django.db import connection
        # cursor = connection.cursor()
        # b = cursor.execute("INSERT INTO productdetail(productname,productorigin,productplatform,merchantid) VALUES( %s, %s, %s, %s )", [ name, origin, platform,merchantid])
        
        
       
 


    
    else:
        return render(request, 'blog/sellerupload.html')# starts from website address
    return render(request, 'blog/sellerupload.html')# starts from website address


#  #admin
#   path('adminprofile/',views.adminprofile, name="adminprofile"),
#   path('adminlistofbuyers/',views.adminlistofbuyers, name="adminlistofbuyers"), 
#   path('adminlistofsellers/',views.adminlistofsellers, name="adminlistofsellers"),
#   path('adminproductlist/',views.adminproductlist, name="adminproductlist"),
#   path('adminproductdetailupdate/<int:id>',views.adminproductdetailupdate, name="adminproductdetailupdate"),
#   path('adminproductdetailpricehistoryupdate/<int:id>',views.adminproductdetailpricehistory, name="adminproductdetailpricehistory"),
 

def adminprofile(request):
    if request.method == "GET":
        return render(request, 'blog/adminprofile.html')
    
def adminlistofbuyers(request):
    if request.method =="POST":
        deletevalue = request.POST.get("deletevalue")
        print(deletevalue)
       
        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:


                

        # Step 1: Delete from Referencing Table (child_table)
            cursor.execute("DELETE FROM blog_profile WHERE user_id = %s", (deletevalue,))

            # Step 2: Delete from Referenced Table (parent_table)
            cursor.execute("DELETE FROM auth_user WHERE id = %s", (deletevalue,))

   
            # Commit the changes
            connection.commit()

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM auth_user')
            productresult = cursor.fetchall()

            connection.commit()
        
        
        return render(request, 'blog/adminlistofbuyers.html',{"productresult": productresult}) 
        

    elif request.method =="GET":

        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM auth_user')
            productresult = cursor.fetchall()

            connection.commit()
        
        
        return render(request, 'blog/adminlistofbuyers.html',{"productresult": productresult}) 
        

def adminlistofsellers(request):
    pass

def adminproductlist(request):
    if request.method =="GET":

        
        
        print("adminproductlist")
        productresult=[]
        priceresult=[]
        tempresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail')
            productresult = cursor.fetchall()

        

            
            for r in productresult:
                print(r[0])
                cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
                priceresult.append(cursor.fetchone())
                #priceresult = priceresult + tempresult
                
            connection.commit()
        print()    
        print(tempresult)
    
        mylist = zip(productresult, priceresult)
        
       

            
            



        print("result")
        print(productresult)
        print(tempresult)

        return render(request, 'blog/adminproductlist.html', {"mylist": mylist}) 
    
def adminproductdetail(request,id):
    if request.method == 'GET':
        searchinput = request.GET.get("searchInput")

        productresult=[]
        priceresult=[]
        

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            productresult = cursor.fetchall()

        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult.append(cursor.fetchone())

            

            connection.commit()
            # for r in productresult:
            #     print(r[0])
            #     cursor.execute('SELECT * FROM pricehistory WHERE productid=%s', (r[0],))
            #     tempresult = cursor.fetchall()
            #     priceresult = priceresult + tempresult
                

        # print()    
        # print(priceresult)
    
        # mylist = zip(productresult, priceresult)
        
       

            
        
        print("result")
        print(productresult)
        print(priceresult)
        return render(request, 'blog/adminproductdetail.html', {"productresult": productresult, "priceresult": priceresult})

def adminproductdetailpricehistory(request):
    pass

def adminproductdetailupdate(request):
    pass


def adminproductdetailpricehistoryupdate(request,id):
    if request.method == "GET":
        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            # cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            # productresult = cursor.fetchall()

        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult = cursor.fetchall()

            
            connection.commit()
            print("price history")
            print(priceresult)

        return render(request, 'blog/adminproductdetailpricehistoryupdate.html', {"priceresult": priceresult})
    
    elif request.method == "POST":
        print("")
        print(id)

        priceupdate = int(request.POST.get("priceupdate"))
        priceid = int(request.POST.get("priceid"))
        print("days")
        print(priceupdate)
        print(priceid)

        productresult=[]
        priceresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            #cursor.execute('SELECT * FROM productdetail WHERE productdetailid=%s', (id,))
            #productresult = cursor.fetchall()
            sql_query = """
                UPDATE pricehistory
                SET price = %s
                WHERE priceid = %s
                """
            params = [priceupdate, priceid]         


            # Execute the raw SQL insert statement and retrieve the ID of the inserted row
            cursor.execute(sql_query, params)
        
            cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (id,))
            priceresult = cursor.fetchall()


            



        return render(request, 'blog/adminproductdetailpricehistoryupdate.html', {"priceresult": priceresult})




def adminspdmpd(request):
    
     

      
        productresult=[]
        priceresult=[]
        tempresult=[]

        from django.db import connection
        with connection.cursor() as cursor:
            # Write your raw SQL insert statement
            cursor.execute('SELECT * FROM productdetail GROUP BY productname')
            productresult = cursor.fetchall()

        

            
            for r in productresult:
                print(r[0])
                cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
                priceresult.append(cursor.fetchone())
                #priceresult = priceresult + tempresult
                
            connection.commit()
        print()    
        print(tempresult)
    
        mylist = zip(productresult, priceresult)
        
       

        print("result")
        print(productresult)
        print(tempresult)

        return render(request, 'blog/adminspdmpd.html', {"mylist": mylist}) 
            

        
        
def groupby(request):
    sql = '''SELECT
    productdetail.productname,
    MAX(pricehistory.price) AS MAX_PRICE,
    MIN(pricehistory.price) AS MIN_PRICE
FROM
    productdetail
JOIN
    pricehistory ON productdetail.productdetailid = pricehistory.productid
GROUP BY
    productdetail.productname;

'''

    productresult=[]
    priceresult=[]
    tempresult=[]

    from django.db import connection
    with connection.cursor() as cursor:
        # Write your raw SQL insert statement
        cursor.execute(sql)
        productresult = cursor.fetchall()

    

        
    #     for r in productresult:
    #         print(r[0])
    #         cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
    #         priceresult.append(cursor.fetchone())
    #         #priceresult = priceresult + tempresult
            
    #     connection.commit()
    # print()    
    # print(tempresult)

    # mylist = zip(productresult, priceresult)
    
    

    print("result")
    print(productresult)
    print(tempresult)

    return render(request, 'blog/groupby.html', {"mylist": productresult}) 
        





# def groupbydetail(request,term):
#     term = request.GET.get(term)
#     if request.method == 'POST':
#         searchinput = request.POST.get("searchInput")
        
#         print("searchinput")
#         print(searchinput)

#         productresult=[]
#         priceresult=[]


       
#         from django.db import connection

#         # Previously it was searched with ILIKE
#         # sql_query = """
#         #     SELECT * FROM productdetail
#         #     WHERE productname ILIKE %s
#         # """


#         # Currently using full_text_search using 

#         # sql_query = """
#         #         SELECT * FROM productdetail
#         #         WHERE to_tsvector('english', productname) @@ to_tsquery('english', %s)
#         # """

#         # Provide the parameter value
#         search_text = request.POST.get("searchInput")


#         # sql_query= '''SELECT *
#         #             FROM your_table
#         #             WHERE to_tsvector('english', your_column) @@ to_tsquery('english', 'your_pattern');
#         #             '''


#         sql_query = """
#                 SELECT * FROM productdetail
#                 WHERE to_tsvector('english', productname) @@ to_tsquery('english', %s)
#         """

#         # Execute the raw SQL query with a prepared statement
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query, [f'%{search_text}%'])
#             productresult = cursor.fetchall()
#             print("Search Results")
#             print(productresult)

#         # from django.db import connection
#         # with connection.cursor() as cursor:
#         #     # Write your raw SQL insert statement ILIKE '%your_text%'SELECT * FROM your_table
#         #     #WHERE your_column ILIKE '%your_text%';
#         #     cursor.execute('SELECT * FROM productdetail WHERE productname ILIKE %s', (searchinput,))
#         #     productresult = cursor.fetchall()

        

#         #     tempresult=[]
#             for r in productresult:
#                 print(r[0])
#                 cursor.execute('SELECT * FROM pricehistory WHERE productid=%s ORDER BY priceid DESC', (r[0],))
#                 priceresult.append(cursor.fetchone())
                
                
#             connection.commit()
#         print()    
#         print(priceresult)
    
#         mylist = zip(productresult, priceresult)
        
       

            
            



#         print("result")
#         print(productresult)
#         print(priceresult)
#         return render(request, 'blog/buyersearchresult.html', {"mylist": mylist})

            

       
#     else:
#         return render(request, 'blog/buyersearch.html')# starts from website address
#     return render(request, 'blog/buyersearch.html')# starts from website address



    