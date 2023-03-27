import React from 'react'
import Project from './Project'

export default function ProjectsPage() {
    return (
        <div className="text-center m-5-auto">
            <h2>Welcome!</h2>
            <form action="/projenter">
                <p className=''>
                    <label>Join an existing project</label>
                    <input type="text" name="existing_proj_id" />
                    <button id="sub_btn" type="submit">Join</button>
                </p>
                <p>
                    <label>Create a new project</label>
                    <input type="text" name="new_proj_id" />
                    <button id="sub_btn" type="submit">Create</button>
                </p>
            <h2>Your Projects</h2>
                <div>
                    <Project />
                </div>
            </form>
        </div>
    )
}