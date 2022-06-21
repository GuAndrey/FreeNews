import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { USERS } from 'src/app/MOCK_DATA_USERS';
import { globals } from 'src/config/globals';
import { User } from './User';

@Injectable({
  providedIn: 'root'
})
export class UserService {
    userList? : User[]
    constructor(private http: HttpClient) { }
    
    getUserById(id: number) : Observable<User> {
        return this.http.get<User>(globals.SERVER + `/user/${id}`, {withCredentials: true})
    }
    
    getUsers(filter: any): Observable<User[]> {
        return this.http.post<User[]>(globals.SERVER + '/userList', filter, {withCredentials: true})
    }
    
    addUserAvatar(avatar: FormData) {
        return this.http.post<{}>(
            globals.SERVER + `/add-user-avatar`,
            avatar, 
            {withCredentials: true}
        );
    }
    
    swapRole(): Observable<User> {
        return this.http.get<User>(`${globals.SERVER}/user/swap-role`, {withCredentials: true})
    }
    
    editDescription(id: number, description: string): Observable<User> {
        return this.http.put<User>(`${globals.SERVER}/user/${id}`, {description}, {withCredentials: true})
    }
}
