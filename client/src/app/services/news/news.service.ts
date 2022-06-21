import { Injectable } from '@angular/core';
import { NEWS } from 'src/app/MOCK_DATA_MATERIALS';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { News } from './News';
import { Observable } from 'rxjs';
import { globals } from 'src/config/globals';

@Injectable({
providedIn: 'root'
})
export class NewsService {
    constructor(private http: HttpClient) { }
    
    getNewsById(id: number) : Observable<News> {
        return this.http.get<News>(globals.SERVER + `/news/${id}`, {withCredentials: true})
    }
    
    getNews(filter: any): Observable<News[]> {
        return this.http.post<News[]>(globals.SERVER + '/newsList', filter, {withCredentials: true})
    }
    
    getNewsByAuthorId(author_id: number) : Observable<News[]> {
        return this.http.post<News[]>(
                globals.SERVER + "/newsList",
                {
                    author_id: author_id,
                }, 
                {withCredentials: true}
            );
    }
    
    addNews(title: string, content: string, region: string, category: string) {
        return this.http.post<News>(
                globals.SERVER + "/news",
                {
                    title: title,
                    content: content,
                    region: region,
                    category: category,
                }, 
                {withCredentials: true}
            );
    }
    
    addNewsResource(resourse: FormData, news_id: number) {
        return this.http.post<News>(
                globals.SERVER + `/add-news-resource/${news_id}`,
                resourse, 
                {withCredentials: true}
            );
    }
    
    deleteNews(news_id: number): Observable<{}> {
        return this.http.delete<{}>(globals.SERVER + `/news/${news_id}`, {withCredentials: true})
    }
    
    getCategorys(): Observable<string[]> {
        return this.http.get<string[]>(globals.SERVER + `/categorys`, {withCredentials: true})
    }
    
    getRegions(): Observable<string[]> {
        return this.http.get<string[]>(globals.SERVER + `/regions`, {withCredentials: true})
    }
}
