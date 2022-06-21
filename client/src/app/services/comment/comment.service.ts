import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { globals } from 'src/config/globals';
import { Comment } from './Comment';
@Injectable({
  providedIn: 'root'
})
export class CommentService {
    constructor(private http: HttpClient) { }
    
    getCommentsByNewsId(news_id: number): Observable<Comment[]> {
        return this.http.get<Comment[]>(globals.SERVER + `/comment/${news_id}`, {withCredentials: true})
    }
    
    addComments(news_id: number, content: string): Observable<Comment> {
        return this.http.post<Comment>(globals.SERVER + `/comment/${news_id}`,
        {
            content: content
        }, 
        {withCredentials: true})
    }
    
    deleteComment(comment_id: number): Observable<{}> {
        return this.http.delete<{}>(globals.SERVER + `/comment/${comment_id}`, {withCredentials: true})
    }
}
