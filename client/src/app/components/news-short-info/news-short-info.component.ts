import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';
import { News } from '../../services/news/News';
import { NewsService } from '../../services/news/news.service';
import { StatService } from '../../services/stat/stat.service';

@Component({
  selector: 'app-news-short-info',
  templateUrl: './news-short-info.component.html',
  styleUrls: ['./news-short-info.component.scss']
})
export class NewsShortInfoComponent implements OnInit {
  @Input() news?: News;

  constructor(
    private newsService: NewsService,
    private statService: StatService,
    private router: Router,
    private eventMagerService: EventManagerService
  ) { }

  ngOnInit(): void {
  }
  
  ngAfterViewChecked(): void {
    this.setNewsContent()
  }
  
  setNewsContent() {
    if (this.news) {
      let contentContainersList = document.getElementsByClassName('content');
      let content = contentContainersList[contentContainersList.length - 1];
      content.innerHTML = this.news.content + '...';
    }
  }
  
  toNewsPage(event: any) {
    const target = <HTMLElement>event.target
    const parentOfTarget = <HTMLElement>target.parentElement
    if (target.classList.contains('stats') || parentOfTarget.classList.contains('stats') || 
        target.classList.contains('delete-btn') || parentOfTarget.classList.contains('delete-btn') ) {
    } else {
      this.router.navigateByUrl("news-page/" + this.news?.id);
    }
  }
  
  private updateNewsStat() {
    if (this.news) {
      this.eventMagerService.statUpdateEmit()
      this.newsService.getNewsById(this.news.id).subscribe(news => {
        this.news = news
      })
    }
  }
  
  swapLike(){
    if (this.news) {
      this.statService.swapLike(this.news.id).subscribe(_ => {
        this.updateNewsStat()
      })
    }
  }
  
  swapRep(){
    if (this.news) {
      this.statService.swapRep(this.news.id).subscribe(_ => {
        this.updateNewsStat()
      })
    }
  }
  
  swapFavorite(){
    if (this.news) {
      this.statService.swapFavorite(this.news.id).subscribe(_ => {
        this.updateNewsStat()
      })
    }
  }
  
  deleteNews() {
    if (this.news)
      this.newsService.deleteNews(this.news.id).subscribe({complete: () => {
        this.eventMagerService.newsDeleteEmit()
        this.news = undefined
      }})
  }
}
