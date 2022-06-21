import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { filter, map } from 'rxjs/operators';
import { AuthService } from 'src/app/services/auth/auth.service';
import { StatService } from 'src/app/services/stat/stat.service';
import { User, UserRole } from 'src/app/services/user/User';
import { UserService } from 'src/app/services/user/user.service';
import { EventManagerService } from '../../services/event-manager/event-manager.service'

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})
export class UserPageComponent implements OnInit {
	UserRole = UserRole
	user?: User;
	userAvatar: FormData = new FormData();
	
	descriptionForm = this.formBuilder.group({
		description: '',
	});
	editDescription = false

	constructor(
		private formBuilder: FormBuilder,
		private userService: UserService,
		private statService: StatService,
		private route: ActivatedRoute,
		private router: Router,
		private eventManagerService: EventManagerService
	) { 
		eventManagerService.userRoleChangeEvent.subscribe(() => {
			this.ngOnInit()
		})
		eventManagerService.statUpdateEvent.subscribe(() => {
			this.getUser();
		})
		eventManagerService.newsDeleteEvent.subscribe(() => {
			this.getUser();
		})
	}

	ngOnInit(): void {
		this.getUser()
		this.router.events.pipe(
			filter(e => e instanceof NavigationEnd)
		).subscribe(() => this.getUser())
	}
	
	ngDoCheck(): void {
		this.setInfoPosition()
	}
	
	setInfoPosition() {
		let container  = <HTMLElement>document.getElementsByClassName('outer')[0];
		let addBtn =  <HTMLElement>document.getElementsByClassName('add-material')[0];
		addBtn.style.left = String(container.offsetLeft + container.offsetWidth + 20) + "px"
	}
	
	getUser(){
		const id = Number(this.route.snapshot.paramMap.get('id'));
		this.userService.getUserById(id).subscribe(user => this.user = user)
	}
	
	addNews() {
		this.router.navigateByUrl("/news-page/editor");
	}
	
	toMenu() {
		this.eventManagerService.openMenuEmit();
	}
	
	onFileSelected(event: any): void {
		const avatar = <File>event.target.files[0]
		this.userAvatar.append('image', avatar, avatar.name);
		this.userService.addUserAvatar(this.userAvatar).subscribe({
			complete: () => {
				this.getUser()
			}
		})
	}
	
	swapSubs(){
		if (this.user) {
			this.statService.swapSub(this.user.id).subscribe(_ => {
				this.getUser();
			})
		}
	}
	
	showEditDescription() {
		this.editDescription = !this.editDescription
		if (this.editDescription) {
			const descriptionInput = <HTMLTextAreaElement>document.getElementById('descriptionInput')
			descriptionInput.value = <string>this.user?.description;
		}
	}
	
	sendDescription(){
		if (this.user) {
			this.userService.editDescription(this.user.id, this.descriptionForm.value.description).subscribe(() => {
				this.editDescription = false
				this.getUser()
			})
		}
	}
}
