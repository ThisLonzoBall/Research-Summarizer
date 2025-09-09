function Layout({children}) {
    return(
        <div className="page">
            <h1 className="title">Researcher Summarizer</h1>
            {children}
        </div>
    )
}

export default Layout;