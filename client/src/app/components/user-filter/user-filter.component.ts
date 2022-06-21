import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { AuthService } from 'src/app/services/auth/auth.service';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';

@Component({
  selector: 'app-user-filter',
  templateUrl: './user-filter.component.html',
  styleUrls: ['./user-filter.component.scss']
})
export class UserFilterComponent implements OnInit {
  
  filterForm = this.formBuilder.group({
    search: '',
    sortBy: 'Подписчикам',
    sortByField: 'Убыванию',
    onlySubs: false,
  });
  
  sortByFieldList = ['Подписчикам', 'Популярности', 'Доверию', 'Просмотрам', 'Кол-во новостей', 'Алфавиту']
  sortByList = ['Убыванию', 'Возрастанию']
  sliderColor: ThemePalette = 'warn'
  authorized = false
  
  @Output() filter = new EventEmitter<FormGroup>();
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private eventManagerService: EventManagerService,
  ) { 
    this.eventManagerService.userChangedEvent.subscribe(() => {
      this.checkAuthorized()
    })
  }

  ngOnInit(): void {
    this.checkAuthorized()
  }
  
  applyFilter(): void {
    this.filter.emit(this.filterForm);
  }
  
  clearFilter(): void {
    this.filterForm = this.formBuilder.group({
      search: '',
      sortBy: 'Подписчикам',
      sortByField: 'Убыванию',
      onlySubs: false,
    });
  }
  
  private checkAuthorized() {
    this.authService.getCurrentId().subscribe(id => {
      this.authorized = id != -1;
    })
  }
}
