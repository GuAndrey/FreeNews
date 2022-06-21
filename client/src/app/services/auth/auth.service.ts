// Необходимые импорты
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { globals } from 'src/config/globals';
import { User } from '../user/User';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }
  
  login(login: string, password: string) : Observable<{}> {
    return this.http.post<{}>(globals.SERVER + "/login", {login: login, password: password}, {withCredentials: true});
  }
  
  registrate(
    mail: string,
    name: string,
    login: string,
    password: string,
    repeat_password: string
  ) {
    return this.http.post<{}>(
      globals.SERVER + "/registration",
      {
        mail: mail,
        login: login,
        name: name,
        password: password,
        repeat_password: repeat_password
      }, 
      {withCredentials: true}
    );
  }
  
  logout() : Observable<{}> {
    return this.http.get<{}>(globals.SERVER + "/logout", {withCredentials: true});
  }
  
  getCurrentId() : Observable<any> {
    return this.http.get(globals.SERVER + "/getCurrentUserId", {withCredentials: true});
  }
}
