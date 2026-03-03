document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentPage = 1;
    let currentLimit = 20;
    let isLoading = false;
    let hasMore = true;

    // Elements
    const grid = document.getElementById('college-grid');
    const searchInput = document.getElementById('search-input');
    const stateSelect = document.getElementById('state-select');
    const ratingSelect = document.getElementById('rating-select');
    const sortSelect = document.getElementById('sort-select');
    const loader = document.getElementById('loading-overlay');
    const loadMoreBtn = document.getElementById('load-more-btn');

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Fetch States for Filter
    async function loadStates() {
        try {
            const res = await fetch('/api/states');
            const data = await res.json();
            if (data.states) {
                data.states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.textContent = state;
                    stateSelect.appendChild(option);
                });
            }
        } catch (e) {
            console.error("Failed to load states", e);
        }
    }

    // Fetch Colleges
    async function fetchColleges(reset = false) {
        if (isLoading) return;
        isLoading = true;
        
        if (reset) {
            currentPage = 1;
            grid.innerHTML = '';
            hasMore = true;
            loadMoreBtn.classList.add('hidden');
        }

        // Show loader if resetting or initial load
        if (reset) loader.classList.remove('hidden');

        const params = new URLSearchParams({
            page: currentPage,
            limit: currentLimit,
            search: searchInput.value,
            state: stateSelect.value,
            rating: ratingSelect.value,
            sort: sortSelect.value
        });

        try {
            const res = await fetch(`/api/colleges?${params.toString()}`);
            const data = await res.json();
            
            if (reset) loader.classList.add('hidden');
            
            if (data.colleges.length > 0) {
                renderCards(data.colleges);
                if (data.colleges.length < currentLimit) {
                    hasMore = false;
                }
            } else {
                hasMore = false;
                if (reset) {
                    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem;">No colleges found matching your criteria.</div>';
                }
            }
            
            if (hasMore) {
                loadMoreBtn.classList.remove('hidden');
            } else {
                loadMoreBtn.classList.add('hidden');
            }

        } catch (e) {
            console.error("Error fetching colleges", e);
            loader.classList.add('hidden');
        } finally {
            isLoading = false;
        }
    }

    // Render Cards
    function renderCards(colleges) {
        colleges.forEach((college, index) => {
            const card = document.createElement('div');
            card.className = 'college-card';
            card.style.animationDelay = `${index * 0.05}s`; // Staggered animation
            
            // Format Fees
            const fees = college.UG_fee ? `₹${college.UG_fee.toLocaleString()}` : 'N/A';
            const approx = college.UG_fee ? 'Approx.' : '';
            
            card.innerHTML = `
                <div class="card-img-placeholder">
                    <i class="fas fa-university"></i>
                </div>
                <div class="card-content">
                    <h3 class="college-name">${college.College_Name}</h3>
                    <div class="college-location">
                        <i class="fas fa-map-marker-alt"></i> ${college.State}
                    </div>
                    
                    <div class="card-badges">
                        <span class="badge badge-rating">
                            <i class="fas fa-star"></i> ${college.Rating}/10
                        </span>
                        <span class="badge badge-fees">
                            ${approx} ${fees} (UG)
                        </span>
                    </div>

                    <div class="card-metrics">
                        <div class="metric">
                            <span class="metric-value">${college.Placement}</span>
                            <span class="metric-label">Placement</span>
                        </div>
                        <div class="metric">
                            <span class="metric-value">${college.Academic}</span>
                            <span class="metric-label">Academic</span>
                        </div>
                        <div class="metric">
                            <span class="metric-value">${college.Infrastructure}</span>
                            <span class="metric-label">Infra</span>
                        </div>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // Event Listeners
    searchInput.addEventListener('input', debounce(() => fetchColleges(true), 500));
    stateSelect.addEventListener('change', () => fetchColleges(true));
    ratingSelect.addEventListener('change', () => fetchColleges(true));
    sortSelect.addEventListener('change', () => fetchColleges(true));
    
    loadMoreBtn.addEventListener('click', () => {
        currentPage++;
        fetchColleges(false);
    });

    // Initial Load
    loadStates();
    fetchColleges(true);
});
