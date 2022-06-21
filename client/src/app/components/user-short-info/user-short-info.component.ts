import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../../services/user/User';
@Component({
  selector: 'app-user-short-info',
  templateUrl: './user-short-info.component.html',
  styleUrls: ['./user-short-info.component.scss']
})
export class UserShortInfoComponent implements OnInit {
  
  @Input() user?: User;

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
  }
  
  toUserPage() {
    this.router.navigateByUrl("user-page/" + this.user?.id);
  }
}
