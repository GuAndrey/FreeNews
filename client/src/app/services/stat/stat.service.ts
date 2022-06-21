import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { globals } from 'src/config/globals';
import { News } from '../news/News';

@Injectable({
  providedIn: 'root'
})
export class StatService {
  constructor(private http: HttpClient) { }
  
  swapLike(news_id: number) {
    return this.http.get<News>(globals.SERVER + `/like/${news_id}`, {withCredentials: true})
  }
  
  swapRep(news_id: number) {
    return this.http.get<News>(globals.SERVER + `/reputation/${news_id}`, {withCredentials: true})
  }
  
  swapFavorite(news_id: number) {
    return this.http.get<News>(globals.SERVER + `/favorite/${news_id}`, {withCredentials: true})
  }
  
  swapSub(sub_id: number) {
    return this.http.get<News>(globals.SERVER + `/subscribe/${sub_id}`, {withCredentials: true})
  }
  
  addView(news_id: number) {
    return this.http.get<News>(globals.SERVER + `/view/${news_id}`, {withCredentials: true})
  }
}
