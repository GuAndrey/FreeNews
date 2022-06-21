import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';
import { News } from '../../services/news/News';
import { NewsService } from '../../services/news/news.service';

@Component({
  selector: 'app-news-list',
  templateUrl: './news-list.component.html',
  styleUrls: ['./news-list.component.scss']
})
export class NewsListComponent implements OnInit {
  newsList: News[] = []
  @Input() author_id?: number;
  
  private filter = {
    search: '',
    startDate: '',
    endDate: '',
    sortBy: 'Дате (сначала новые)',
    region: 'Любой',
    category: 'Любая',
    onlyFavotite: false,
    onlySubs: false,
  }

  constructor(
    private newsService: NewsService,
  ) {}
  
  ngOnInit(): void {
    if (!this.author_id) {
      this.getNews()
    }
  }
  
  ngOnChanges(): void {
    if (this.author_id) {
      this.getNewsByAuthorId(this.author_id)
    } else {
      this.getNews()
    }
  }
  
  ngDoCheck(): void {
    this.setFilterPosition()
  }
  
  setFilterPosition() {
    let container  = <HTMLElement>document.getElementsByClassName('list-conteinr-inner')[0];
    let filter =  <HTMLElement>document.getElementsByClassName('news-filter')[0];
    if (filter && container)
      filter.style.left = String(container.offsetLeft + container.offsetWidth + 20) + "px";
  }
  
  getNewsByAuthorId(author_id: number) {
    this.newsService.getNewsByAuthorId(author_id)
      .subscribe(newsList => this.newsList = newsList);
  }
  
  getNews(){
    this.newsService.getNews(this.filter)
      .subscribe(newsList => {
        this.newsList = newsList
      });
  }
  
  changeFilter(filter: FormGroup) {
    this.filter = filter.value;
    this.getNews()
  }
}
