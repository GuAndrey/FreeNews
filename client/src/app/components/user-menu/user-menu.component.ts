import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { BaseForm } from 'src/app/base-class/base-form';
import { AuthService } from 'src/app/services/auth/auth.service';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';
import { User, UserRole } from 'src/app/services/user/User';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss']
})
export class UserMenuComponent extends BaseForm implements OnInit {
  private user?: User;
  roleToSwap = 'автором';

  constructor(
    private authService: AuthService,
    private userService: UserService,
    eventManagerService: EventManagerService,
  ) { 
    super(eventManagerService);
  }
  
  ngOnInit(): void {
    this.authService.getCurrentId().subscribe(id => {
      this.userService.getUserById(id).subscribe(user => {
        this.user = user
        this.changeRoleToSwap()
      })
    })
  }
  
  swapRole(): void {
    this.userService.swapRole().subscribe((user) => {
      if (this.user) {
        this.user.role = user.role
        this.changeRoleToSwap()
      }
    })
  }
  
  private changeRoleToSwap() {
    if (this.user)
      switch (this.user.role) {
        case (UserRole.AUTHOR):
          this.roleToSwap = 'читателем';
          break;
        case (UserRole.READER):
          this.roleToSwap = 'автором';
          break;
        default:
          this.roleToSwap = 'автором';
          break;
    }
    this.eventManagerService.userRoleChangeEmit();
  }
  
  logout(): void {
		this.authService.logout().subscribe(() => {
      this.eventManagerService.userChangedEmit();
			window.location.href = "/";
		})
	}
}
