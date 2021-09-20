iterface MenuMain{
    path : string
    mate:Mate
    hidden?:boolean
}

iterface MenuItem {
    current : MenuMain[] | null
}

const asidMenu = ref<MenuItem>({current:null})