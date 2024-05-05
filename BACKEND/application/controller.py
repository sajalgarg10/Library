from application import app
from flask import request , jsonify ,  abort
from application.database import User , jwt , Section , Book,  db, Request , Return ,IssuedTo , Feedback , cach ,  IssuedData
from werkzeug.security import check_password_hash , generate_password_hash
from flask import request, jsonify
from flask_jwt_extended import   create_access_token , jwt_required, get_jwt_identity , get_jwt
from flask_cors import cross_origin
from sqlalchemy import or_
from datetime import datetime
import re
from sqlalchemy import func
import json






@app.route("/" , methods = ['GET','POST'])
@cross_origin(origin='*')
def login():
    if request.method == "GET":
        return jsonify({"msg":"please login"})
    if request.method == 'POST':
        try:
            username = request.json['username']
            username = username.strip()
            password = request.json['password']
            login_obj = User.query.filter_by(username = username).first()
            if login_obj:
                print("login obj is fine ")
                if login_obj.role == "librarian"and check_password_hash( login_obj.password , password): 
                    print("inside librarian")
                    login_obj.last_visit = datetime.now()
                    # login_user(login_obj)
                    access_token = create_access_token(identity= {"id": login_obj.user_id , "username": login_obj.username , "password":login_obj.password , "role": login_obj.role})
                    result = {'access_token': access_token , "message": "login successful" , "user": "librarian"}
                    db.session.commit()
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp 
                else:
                    result = {"message": "User is not authorised"}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp    
                # else:
                #     result = {"message": "password does not match"}
                #     resp = jsonify(result)
                #     resp.status_code = 401
            else:
                result = {"message": "User does not exist"}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
        except:
            abort(404)

@app.route("/user" , methods = ['POST'])
@cross_origin(origin='*')
def user_login():
    if request.method == 'POST':
        try:
            username = request.json['username']
            username = username.strip()
            password = request.json['password']
            login_obj = User.query.filter_by(username = username).first()
            #db.session.query(User).filter(username = username).first()
            if login_obj:
                print("login obj is fine ")
                if check_password_hash(login_obj.password,  password  ) :
                    print("password condintion is right")
                    login_obj.last_visit = datetime.now()
                    access_token = create_access_token(identity= {"id": login_obj.user_id , "username": login_obj.username , "password":login_obj.password , "role": login_obj.role})
                    result = {"access_token": access_token , "message": "login successful"}
                    db.session.commit()
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp
                else:
                    result = {"message": "password does not match"}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp 

            else:
                result = {"message": "User does not exist"}
                resp = jsonify(result)
                resp.status_code = 401
                return resp 
        except:
            abort(404)


blacklisted_tokens = set()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens
    

@app.route("/logout", methods = ["GET","POST"])
@cross_origin(origin='*')
@jwt_required()
def logout():
    try:
        if request.method == "GET":
            current_user_id = get_jwt_identity()
            if current_user_id:
                jti = get_jwt()['jti']
                blacklisted_tokens.add(jti)
                result = {"message": "logout successful"}
                resp = jsonify(result)
                resp.status = 200
                return resp 
            else:
                result = {"message": "user currently not login session"}
                resp = jsonify(result)
                resp.status_code = 401
                return resp 
    except:
        abort(404)

@app.route('/register', methods = ['POST'])
def register():
    try:
        if request.method == "POST":
            username = request.json["username"]
            #username = username.strip()
            print(username)
            password = request.json["password"]
            #role = request.json["role"]
            register_obj = User.query.filter_by(username = username).first()
            if register_obj is None:
                if username is not None and username != " ":
                    if password is not None and re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
                        passw = generate_password_hash(password)
                        user = User(username = username , password = passw , role = "user", number_of_books = 0, last_visit = datetime.now())
                        db.session.add(user)
                        db.session.commit()
                        result = {"meaasge": "New User is successfully created"}
                        resp = jsonify(result)
                        resp.status_code = 200
                        return resp
                    else:
                        result = {"meaasge": "invalid password"}
                        resp = jsonify(result)
                        resp.status_code = 401
                        return resp
                else:
                    result = {"meaasge": "invalid username"}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"meaasge": "user already exist"}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except:
        abort(400)       



@app.route("/admin_dashboard/home", methods = ['GET'])
@jwt_required()
@cach.cached(timeout=5)
def dashboard():
    try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            if "librarian" in user_roles:
                sec = Section.query.all()
                result = []
                for i in range(len(sec)):
                    el = {}
                    el["section"] = sec[i].name 
                    el["description"] = sec[i].description
                    el["books"] = []
                    el["id"] = sec[i].id
                    for j in sec[i].book:
                        d = []
                        d.append(j.name)
                        d.append(j.content)
                        d.append(j.author)
                        d.append(j.id)
                        feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                        print(feed_obj)
                        feed_list = []
                        for k in feed_obj:
                            feed_dict = {}
                            feed_dict["username"] = k[0]
                            feed_dict["feed"] = k[1]
                            feed_list.append(feed_dict)
                        d.append(feed_list)
                        el["books"].append(d)  
                    result.append(el)
                print(result)        
                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)  





@app.route("/admin_dashboard/access", methods = ['GET'])
@cross_origin(origin='*')
@cach.cached(timeout=5)
@jwt_required()
def access():
    try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("current user working ")
            user_roles = current_user.get('role', [])
            if 'librarian' in user_roles:
                print("libarion")
                request_obj = db.session.query(User.username , Request.user_id , Book.name ,Request.book_id).join(Request, User.user_id == Request.user_id).join(Book, Request.book_id == Book.id).all()
                print(request_obj)
                return_obj = db.session.query(User.username,  Return.user_id , Book.name , Return.book_id).join(Return, User.user_id == Return.user_id).join(Book, Return.book_id == Book.id).all()
                print(return_obj)
                isuued_to = db.session.query(User.username,  IssuedTo.issued_user , Book.name , IssuedTo.issued_book).join(IssuedTo, User.user_id == IssuedTo.issued_user).join(Book, IssuedTo.issued_book == Book.id).all()
                print(isuued_to)
                result = {}
                result["request"]= []
                result["return"]= []
                result["issued"] = []
                for i in range(len(request_obj)):
                    d= {}
                    d["user_name"] = request_obj[i][0]
                    d["user_id"] = request_obj[i][1]
                    d["book_name"] = request_obj[i][2]
                    d["book_id"] = request_obj[i][3] 
                    result["request"].append(d)


                for i in range(len(return_obj)):
                    d= {}
                    d["user_name"] = return_obj[i][0]
                    d["user_id"] = return_obj[i][1]
                    d["book_name"] = return_obj[i][2]
                    d["book_id"] = return_obj[i][3]
                    result["return"].append(d)     

                for i in range(len(isuued_to)):
                    d= {}
                    d["user_name"] = isuued_to[i][0]
                    d["user_id"] = isuued_to[i][1]
                    d["book_name"] = isuued_to[i][2]
                    d["book_id"] = isuued_to[i][3]
                    result["issued"].append(d)  
               
                resp = jsonify(result)
                resp.status_code = 200
                return resp    
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)  

@app.route("/admin_dashboard/home/search/<string:q>", methods = ['GET',"POST"])
@jwt_required()
def admin_search(q):
    try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            if "user" in user_roles or 'librarian' in user_roles:
                serr = Section.query.filter(Section.name.ilike(f'%{q}%') ).all()
                serr_b = Book.query.filter(or_(Book.name.ilike(f'%{q}%'),Book.content.ilike(f'%{q}%'), Book.author.ilike(f'%{q}%')  )).all()
                result = []
                print(serr_b)
                print(serr)
                if serr is not None:
                    for i in range(len(serr)):
                        el = {}
                        el["section"] = serr[i].name 
                        el["description"] = serr[i].description
                        el["books"] = []
                        el["id"] = serr[i].id
                        for j in serr[i].book:
                            d = []
                            d.append(j.name)
                            d.append(j.content)
                            d.append(j.author)
                            d.append(j.id)
                            feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                            feed_list = []
                            for k in feed_obj:
                                feed_dict = {}
                                feed_dict["username"] = k[0]
                                feed_dict["feed"] = k[1]
                                feed_list.append(feed_dict)
                            d.append(feed_list)
                            el["books"].append(d)
                        result.append(el)    
                if serr_b is not None:
                    s = set()
                    for i in serr_b:
                        s.add(i.id)   
                    for i in range(len(serr_b)):
                        sec = Section.query.filter_by(id = serr_b[i].section).first()
                        el = {}
                        el["section"] = sec.name 
                        el["description"] = sec.description
                        el["books"] = []
                        el["id"] = sec.id
                        for j in sec.book:
                            print(j)
                            if j.id in s:
                                d = []
                                d.append(j.name)
                                d.append(j.content)
                                d.append(j.author)
                                d.append(j.id)
                                feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                                feed_list = []
                                for k in feed_obj:
                                    feed_dict = {}
                                    feed_dict["username"] = k[0]
                                    feed_dict["feed"] = k[1]
                                    feed_list.append(feed_dict)
                                d.append(feed_list)
                                el["books"].append(d)
                        result.append(el) 
                    print(result)          
                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)          






@app.route("/admin_dashboard/access/grant/<int:id>", methods = ['GET','POST'])
@cross_origin(origin='*')
@jwt_required()
def grant(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            print("current user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            if 'librarian' in user_roles:
                print(user_roles)
                request_obj = Request.query.filter_by(user_id = id).first()
                print(request_obj)
                user_obj = User.query.filter_by(user_id = id).first()
                if user_obj.number_of_books < 5:
                    issue_obj = IssuedTo(issued_book = request_obj.book_id , issued_user = request_obj.user_id)
                    issue_hist = IssuedData(issued_book = request_obj.book_id , issued_user = request_obj.user_id)
                    user_obj.number_of_books = user_obj.number_of_books + 1
                    db.session.delete(request_obj)
                    db.session.add(issue_obj)
                    db.session.add(issue_hist)
                    db.session.commit()
                    result = {"message": "User granted access"}
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp 
                else:
                    db.session.delete(request_obj)
                    db.session.commit()
                    result = {"message": "User exccedd number of books "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp 


            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)




@app.route("/admin_dashboard/access/return/<int:id>", methods = ['POST'])
@cross_origin(origin='*')
@jwt_required()
def revoke_return(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            print("current user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
     
            if 'librarian' in user_roles:
                return_obj = Return.query.filter_by(user_id = id).first()
                print(return_obj)
                user_obj = User.query.filter_by(user_id = id).first()
                print(user_obj)
                issue_obj = IssuedTo.query.filter_by(issued_user = id).first()
                print(issue_obj)
                db.session.delete(issue_obj)
                db.session.delete(return_obj)
                user_obj.number_of_books = user_obj.number_of_books - 1
                db.session.commit()
                result = {"message": "User return successful"}
                resp = jsonify(result)
                resp.status_code = 200
                return resp   
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)

@app.route("/admin_dashboard/access/revoke/<int:id>", methods = ['POST'])
@cross_origin(origin='*')
@jwt_required()
def revoke(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            print("current user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            if 'librarian' in user_roles:
                user_obj = User.query.filter_by(user_id = id).first()
                print(user_obj)
                issue_obj = IssuedTo.query.filter_by(issued_user = id).first()
                print(issue_obj)
                db.session.delete(issue_obj)
                user_obj.number_of_books = user_obj.number_of_books - 1
                db.session.commit()
                result = {"message": "User access revoked"}
                resp = jsonify(result)
                resp.status_code = 200
                return resp   
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)


@app.route("/admin_dashboard/access/decline/<int:id>", methods = ['POST'])
@cross_origin(origin='*')
@jwt_required()
def decline(id):
    try:
        if request.method == 'POST':
            print("inside if condition")
            current_user = get_jwt_identity()
            print("current user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            if 'librarian' in user_roles:
                print("inside loop")
                req_obj = Request.query.filter_by(user_id = id).first()
                print(req_obj)
                db.session.delete(req_obj)
                db.session.commit()
                result = {"message": "User access revoked"}
                resp = jsonify(result)
                resp.status_code = 200
                return resp   
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)        






@app.route("/user/dashboard/home", methods = ['GET'])
@cross_origin(origin='*')
@jwt_required()
@cach.cached(timeout=5)
def user_dashboard():
    try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
                
            if 'user' in user_roles or 'librarian' in user_roles:
                sec = Section.query.all()
                result = []
                for i in range(len(sec)):
                    el = {}
                    el["section"] = sec[i].name
                    el["description"] = sec[i].description
                    el["books"] = []
                    print(el)
                    for j in sec[i].book:
                        d = []
                        d.append(j.id)
                        d.append(j.name)
                        d.append(j.content)
                        d.append(j.author)
                        feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                        feed_list = []
                        for k in feed_obj:
                            feed_dict = {}
                            feed_dict["username"] = k[0]
                            feed_dict["feed"] = k[1]
                            feed_list.append(feed_dict)
                        d.append(feed_list)
                        el["books"].append(d)
                        print(el)
                    result.append(el)    
                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)  


@app.route("/user/dashboard/home/request/<int:id>", methods = ['POST'])
@cross_origin(origin='*')
@jwt_required()
def request_(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            u_id = current_user.get("id",[])
            print(u_id)
            retu = Request(user_id = u_id , book_id = id)
            db.session.add(retu)
            db.session.commit()
            resp = jsonify({"message":"successful added"})
            resp.status_code = 200
            return resp
        # else:
        #     result = {"message": "Unauthorized user "}
        #     resp = jsonify(result)
        #     resp.status_code = 401
        #     return resp
    except: 
        abort(404)  

@app.route("/user/dashboard/home/feedback/<int:id>", methods = ['POST'])
@cross_origin(origin='*')
@jwt_required()
def feedback(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            feed =  request.json["feed"]
            if feed is not None and feed != ' ':
                print("cureent user working ")
                print(current_user)
                user_roles = current_user.get('role', [])
                print(user_roles)
                u_id = current_user.get("id",[])
                print(u_id)
                feed_obj = Feedback(feed = feed, user_id = u_id , book_id = id)
                db.session.add(feed_obj)
                db.session.commit()
                resp = jsonify({"message":"successful added"})
                resp.status_code = 200
                return resp
            else:
                result = {"message": "invalid input "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp

        # else:
        #     result = {"message": "Unauthorized user "}
        #     resp = jsonify(result)
        #     resp.status_code = 401
        #     return resp
    except: 
        abort(404)          

@app.route("/user/dashboard/issued", methods = ['GET'])
@cross_origin(origin='*')
@jwt_required()
def issued():
    #try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles) 
            if 'user' in user_roles or 'librarian' in user_roles:
                id = current_user.get("id")
                iss = db.session.query(User.username , IssuedTo.issued_user , Book.name ,IssuedTo.issued_book, Book.book_).join(IssuedTo, User.user_id == IssuedTo.issued_user).join(Book, IssuedTo.issued_book == Book.id).filter(User.user_id == id).all()
                result = []
                for i in range(len(iss)):
                    d = {}
                    d["user_name"] = iss[i][0]
                    d["user_id"] = iss[i][1]
                    d["book_name"] = iss[i][2]
                    d["book_id"] = iss[i][3]
                    d["book"] = iss[i][4]
                    result.append(d)  

                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    # except: 
    #     abort(404)  

@app.route("/user/dashboard/issued/return/<int:id>", methods = ['GET','POST'])
@cross_origin(origin='*')
@jwt_required()
def return_(id):
    try:
        if request.method == 'POST':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles) 
            if 'user' in user_roles or 'librarian' in user_roles:
                print("in loop")
                u_id = current_user.get("id")
                print(u_id)
                retu = Return(user_id = u_id , book_id = id)
                print(retu)
                db.session.add(retu)
                db.session.commit()

                result = {"message": "Return request succeefully sent "}
                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)          




@app.route("/admin_dashboard/home/add_section", methods = ['GET', 'POST'])
@cross_origin(origin='*')
@jwt_required()
def add_section():
    try:
        if request.method == 'POST':
            name = request.json["name"]
            description = request.json["description"]
            if name is not None and name != " ":
                current_user = get_jwt_identity()
                user_roles = current_user.get('role', [])
                if 'librarian' in user_roles:
                    sec_obj = Section.query.filter_by(name = name).first()
                    print(sec_obj)
                    print("query cate object in database")
                    if sec_obj is None:
                        print("if condition")
                        sec = Section(name = name , description= description )
                        db.session.add(sec)
                        db.session.commit()
                        result = {"message": "Section successfullu added"}
                        resp = jsonify(result)
                        resp.status_code = 200
                        return resp
                    else:
                        result = {"message": "Section Allready exixts "}
                        resp = jsonify(result)
                        resp.status_code = 401
                        return resp
                else:
                    result = {"message": "Unauthorized user "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"message": "invalid input "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp

    except: 
        abort(404)  


@app.route("/admin_dashboard/home/update_section/<int:id>", methods = ['GET', 'PUT'])
@cross_origin(origin='*')
@jwt_required()
def update_section(id):
    try:
        if request.method == 'PUT':
            name = request.json["name"]
            des = request.json["description"]
            if name is not None and name != " ":

                current_user = get_jwt_identity()
                user_roles = current_user.get('role', [])
                if 'librarian' in user_roles:
                    sec_obj =   Section.query.filter_by(id = id).first()
                    print(sec_obj)
                    print("query cate object in database")
                    if sec_obj:
                        print("if condition")
                        sec_obj.name = name
                        sec_obj.description = des
                        db.session.commit()
                        result = {"message": "Section successfully updated"}
                        resp = jsonify(result)
                        resp.status_code = 200
                        return resp
                    else:
                        result = {"message": "Section Allready exixts "}
                        resp = jsonify(result)
                        resp.status_code = 401
                        return resp
                else:
                    result = {"message": "Unauthorized user "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"message": "invalid input "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp

    except: 
        abort(404)  


@app.route("/admin_dashboard/home/delete_section/<int:id>", methods = ['GET', 'DELETE'])
@cross_origin(origin='*')
@jwt_required()
def delete_section(id):  
    try:
        if request.method == 'DELETE':
            current_user = get_jwt_identity()
            user_roles = current_user.get('role', [])
            if 'librarian' in user_roles:
                section_to_delete = Section.query.filter_by(id = id).first()
                print(section_to_delete)
                if section_to_delete:
                    print("inside the loop")
                    db.session.delete(section_to_delete)
                    db.session.commit()
                    result = {"message": "Section successfully deleted "}
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp
                else:
                    result = {"message": "Section does not exixts "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)  



@app.route("/admin_dashboard/home/add_book/<int:id>", methods = ['GET', 'POST'])
@cross_origin(origin='*')
@jwt_required()
def add_book(id):
    try:
        if request.method == 'POST':
            name = request.json["name"]
            content = request.json["content"]
            author = request.json["author"]
            book_ = request.json["book"]
            if name is not None and name != " " and author is not None and author != " " and book_ is not None and book_ != " ":
                current_user = get_jwt_identity()
                user_roles = current_user.get('role', [])
                if 'librarian' in user_roles:
                    book_obj = Book.query.filter_by(name = name ).first()
                    print(book_obj)
                    print("query cate object in database")
                    if book_obj is None:
                        print("if condition")
                        prod = Book(name = name , content = content , author = author, section = id , book_ = book_)
                        db.session.add(prod)
                        db.session.commit()
                        result = {"message": "Book successfully added"}
                        resp = jsonify(result)
                        resp.status_code = 200
                        return resp
                    else:
                        result = {"message": "Book Allready exixts "}
                        resp = jsonify(result)
                        resp.status_code = 401
                        return resp
                else:
                    result = {"message": "Unauthorized user "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"message": "invalid input "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
                
    except: 
        abort(404)  




@app.route("/admin_dashboard/home/update_book/<int:id>", methods = ['GET', 'PUT'])
@cross_origin(origin='*')
@jwt_required()
def update_book(id):
    try:
        if request.method == 'PUT':
            name = request.json["name"]
            content = request.json["content"]
            author = request.json["author"]
            book_ = request.json["book"]
            if name is not None and name != " " and author is not None and author != " " and book_ is not None and book_ != " ":
                current_user = get_jwt_identity()
                user_roles = current_user.get('role', [])
                if 'librarian' in user_roles:
                    book_obj = Book.query.filter_by(id = id).first()
                    print(book_obj)
                    print("query cate object in database")
                    if book_obj:
                        print("if condition")
                        book_obj.name = name
                        book_obj.content = content
                        book_obj.author = author
                        book_obj.book_ = book_
                        db.session.commit()
                        result = {"message": "Book successfullu updated"}
                        resp = jsonify(result)
                        resp.status_code = 200
                        return resp
                    else:
                        result = {"message": "Book Allready exixts "}
                        resp = jsonify(result)
                        resp.status_code = 401
                        return resp
                else:
                    result = {"message": "Unauthorized user "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                    result = {"message": "invalid input"}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp    
    except: 
        abort(404)    


@app.route("/admin_dashboard/home/delete_book/<int:id>", methods = ['GET', 'DELETE'])
@cross_origin(origin='*')
@jwt_required()
def delete_book(id):  
    try:
        if request.method == 'DELETE':
            current_user = get_jwt_identity()
            user_roles = current_user.get('role', [])
            if 'librarian' in user_roles:
                Book_to_delete = Book.query.filter_by(id = id).first()
                if Book_to_delete:
                    print("inside the loop")
                    db.session.delete(Book_to_delete)
                    db.session.commit()
                    result = {"message": "Book successfully deleted "}
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp
                else:
                    result = {"message": "Book does not exixts "}
                    resp = jsonify(result)
                    resp.status_code = 401
                    return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)  




@app.route("/user/dashboard/home/search/<string:q>", methods = ['GET',"POST"])
@jwt_required()
def user_search(q):
    try:
        if request.method == 'GET':
            current_user = get_jwt_identity()
            print("cureent user working ")
            print(current_user)
            user_roles = current_user.get('role', [])
            print(user_roles)
            if "user" in user_roles or 'librarian' in user_roles:
                serr = Section.query.filter(Section.name.ilike(f'%{q}%') ).all()
                serr_b = Book.query.filter(or_(Book.name.ilike(f'%{q}%'),Book.content.ilike(f'%{q}%'), Book.author.ilike(f'%{q}%')  )).all()
                result = []
                print(serr_b)
                print(serr)
                if serr is not None:
                    for i in range(len(serr)):
                        el = {}
                        el["section"] = serr[i].name 
                        el["description"] = serr[i].description
                        el["books"] = []
                        el["id"] = serr[i].id
                        for j in serr[i].book:
                            d = []
                            d.append(j.name)
                            d.append(j.content)
                            d.append(j.author)
                            d.append(j.id)
                            feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                            feed_list = []
                            for k in feed_obj:
                                feed_dict = {}
                                feed_dict["username"] = k[0]
                                feed_dict["feed"] = k[1]
                                feed_list.append(feed_dict)
                            d.append(feed_list)
                            el["books"].append(d)
                        result.append(el)    
                if serr_b is not None:
                    s = set()
                    for i in serr_b:
                        s.add(i.id)   
                    for i in range(len(serr_b)):
                        sec = Section.query.filter_by(id = serr_b[i].section).first()
                        el = {}
                        el["section"] = sec.name 
                        el["description"] = sec.description
                        el["books"] = []
                        el["id"] = sec.id
                        for j in sec.book:
                            print(j)
                            if j.id in s:
                                d = []
                                d.append(j.name)
                                d.append(j.content)
                                d.append(j.author)
                                d.append(j.id)
                                feed_obj = db.session.query(User.username , Feedback.feed).join(Feedback, User.user_id == Feedback.user_id).filter(Feedback.book_id == j.id).all()
                                feed_list = []
                                for k in feed_obj:
                                    feed_dict = {}
                                    feed_dict["username"] = k[0]
                                    feed_dict["feed"] = k[1]
                                    feed_list.append(feed_dict)
                                d.append(feed_list)
                                el["books"].append(d)
                        result.append(el) 
                    print(result)          
                resp = jsonify(result)
                resp.status_code = 200
                return resp
            else:
                result = {"message": "Unauthorized user "}
                resp = jsonify(result)
                resp.status_code = 401
                return resp
    except: 
        abort(404)          


@app.route("/user/dashboard/summary", methods = ["GET"])
@jwt_required()
def user_sum():
    try:
        summ = []
        if request.method == 'GET':
            req = db.session.query(Book.name, func.count(IssuedTo.issued_book)).join(IssuedTo, Book.id == IssuedTo.issued_book).group_by(Book.name).all()
            feed = db.session.query(Book.name, func.count(Feedback.book_id)).join(Feedback, Book.id == Feedback.book_id).group_by(Book.name).all()
            print(req)
            print(feed)
            l_req = []
            l_feed = []
            l_book = []
            for i in req:
                l_req.append(i[1])
           
            for i in feed:
                l_book.append(i[0])
                l_feed.append(i[1])
            summ.append(l_book) 
            summ.append(l_req)   
            summ.append(l_feed)
            print(summ)
            resp = jsonify(summ)
            resp.status_code = 200
            return resp
    except:
        abort(404)


@app.route("/admin_dashboard/summary", methods = ["GET"])
@jwt_required()
def admin_sum():
    try:
        summ = []
        if request.method == 'GET':
            print("aaaaaa")
            req = db.session.query(Book.name, func.count(IssuedTo.issued_book)).join(IssuedTo, Book.id == IssuedTo.issued_book).group_by(Book.name).all()
            print("hhhhhhhhh")
            feed = db.session.query(Book.name, func.count(Feedback.book_id)).join(Feedback, Book.id == Feedback.book_id).group_by(Book.name).all()
            print("hhhhlkgjlhhh")
            print(req)
            print(feed)
            l_book = []
            l_req = []
            l_feed = []
            for i in req:
                l_req.append(i[1])
            for i in feed:
                l_book.append(i[0])
                l_feed.append(i[1])
            summ.append(l_book) 
            summ.append(l_req)   
            summ.append(l_feed)
            print(summ)
            resp = jsonify(summ)
            resp.status_code = 200
            return resp
    except:
        abort(404)
