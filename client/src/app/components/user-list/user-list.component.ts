import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { User } from 'src/app/services/user/User';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {
  userList : User[] = []

  private filter = {
    search: '',
    sortBy: 'Подписчикам',
    sortByField: 'Убыванию',
    onlySubs: false,
  };
  constructor(private userService: UserService, private formBuilder: FormBuilder) { }
  
  ngOnInit(): void {
    this.getUsers()
  }
  
  ngDoCheck(): void {
    this.setFilterPosition()
  }
  
  getUsers(){
    this.userService.getUsers(this.filter).subscribe(userList => this.userList = userList)
  }
  
  setFilterPosition() {
    let container  = <HTMLElement>document.getElementsByClassName('list-conteinr-inner')[0];
    let filter =  <HTMLElement>document.getElementsByClassName('user-filter')[0];
    if (filter && container)
      filter.style.left = String(container.offsetLeft + container.offsetWidth + 20) + "px";
  }
  
  changeFilter(filter: FormGroup) {
    this.filter = filter.value;
    this.getUsers()
  }
}
