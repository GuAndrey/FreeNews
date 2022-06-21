import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { AuthService } from 'src/app/services/auth/auth.service';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';
import { NewsService } from 'src/app/services/news/news.service';

@Component({
  selector: 'app-news-filter',
  templateUrl: './news-filter.component.html',
  styleUrls: ['./news-filter.component.scss']
})
export class NewsFilterComponent implements OnInit {
  
  filterForm = this.formBuilder.group({
    search: '',
    startDate: '',
    endDate: '',
    sortBy: 'Дате (сначала новые)',
    region: 'Любой',
    category: 'Любая',
    onlyFavotite: false,
    onlySubs: false,
  });
  
  sortByList = ['Дате (сначала новые)', 'Дате (сначала старые)', 'Популярности (убыв.)', 'Популярности (возр.)', 'Достоверности (убыв.)', 'Достоверности (возр.)', 'Просмотрам (убыв.)', 'Просмотрам (возр.)']
  regions: string[] = ['Любой']
  categorys: string[] = ['Любая']
  sliderColor: ThemePalette = 'warn'
  authorized = false
  
  @Output() filter = new EventEmitter<FormGroup>();
  constructor(
    private formBuilder: FormBuilder,
    private newsService: NewsService,
    private authService: AuthService,
    private eventManagerService: EventManagerService,
  ) { 
    this.eventManagerService.userChangedEvent.subscribe(() => {
      this.checkAuthorized()
    })
  }
  
  ngOnInit(): void {
    this.newsService.getRegions().subscribe(regions => {
      this.regions.push(...regions);
    })
    this.newsService.getCategorys().subscribe(categorys => {
        this.categorys.push(...categorys);
    })
    this.checkAuthorized()
  }
  
  applyFilter(): void {
    this.filter.emit(this.filterForm);
  }
  
  clearFilter(): void {
    this.filterForm = this.formBuilder.group({
      search: '',
      startDate: '',
      endDate: '',
      sortBy: 'Дате (сначала новые)',
      region: 'Любой',
      category: 'Любая',
      onlyFavotite: false,
      onlySubs: false,
    });
  }
  
  private checkAuthorized() {
    this.authService.getCurrentId().subscribe(id => {
      this.authorized = id != -1;
    })
  }
}
