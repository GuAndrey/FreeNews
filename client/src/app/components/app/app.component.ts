import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';
import { UserService } from '../../services/user/user.service';
import { EventManagerService } from '../../services/event-manager/event-manager.service'
import { FormType } from 'src/app/base-class/base-form';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title = 'FREENEWS';
  login : string = "Войти";
  to_login : boolean = false;
  to_reg : boolean = false;
  to_menu : boolean = false;

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private router: Router,
    private eventManagerService: EventManagerService,
  ) {
    eventManagerService.switchFormEvent.subscribe( formType => {
      this.switchForm(formType)
    })
    eventManagerService.closeFormEvent.subscribe(() => {
      this.closeAllForm();
    })
    eventManagerService.userChangedEvent.subscribe(() => {
      this.setLogin();
    })
    eventManagerService.openMenuEvent.subscribe(() => {
      this.openMenu()
    })
  }

  ngOnInit() {
    this.setLogin()
  }

  setLogin() {
    this.authService.getCurrentId().subscribe(user_id => {
      if (user_id == -1) {
        this.login = 'Войти'
      } else {
        this.userService.getUserById(user_id).subscribe(user => {
          this.login = user.login
        });
      }
      this.closeAllForm();
    })
  }

  onLogin() {
    this.authService.getCurrentId().subscribe(user_id => {
      if (user_id == -1 ) {
        this.toLoginForm()
      } else {
        this.router.navigateByUrl("user-page/" + user_id);
      }
    })
  }

  openMenu() {
    this.toMenuForm();
  }

  switchForm(event: FormType) {
    switch (event) {
      case FormType.REG:
        this.toRegForm()
        break;
      case FormType.LOGIN:
        this.toLoginForm()
        break;
      case FormType.MENU:
        this.toMenuForm()
        break;
      default:
        this.closeAllForm();
        break;
    }
  }

  private closeAllForm() {
    this.to_login = false
    this.to_reg = false
    this.to_menu = false
  }

  private toLoginForm() {
    this.closeAllForm();
    this.to_login = true;
  }

  private toRegForm() {
    this.closeAllForm();
    this.to_reg = true;
  }

  private toMenuForm() {
    this.closeAllForm();
    this.to_menu = true;
  }
}
